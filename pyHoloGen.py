
# 
# This file is part of pyHoloGen. 
# Copyright (C) 2015-2018  Svetlin Tassev
# 						 Braintree High School
#						 Harvard-Smithsonian Center for Astrophysics
# 
#    pyHoloGen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#   
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#   
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#   
# 

from holo_sum import transform_with_phase
import numpy as np

def calculate_hologram(object_amplitude_in, object_position_x, object_position_y, object_position_z,
	holo_aperture_x,holo_aperture_y,res_x,res_y,wavelength,
	RANDOM=True,ATTENUATION=True,N_SA=10,
	FRACTON_SA_BURN=0.71,POINT_SOURCE_DISTANCE=1.e8,AMPL_FLUCT=0.1,METHOD='real'):

	# object_amplitude_in: brightness of each object to be imaged.
	#
	# object_position_i: 1D arrays giving (x,y,z) of the objects to be 
	# imaged in the hologram in meters 

	# holo_aperture_i is the physical size of the hologram in meters. It 
	# is centered a (x,y,z)=(0,0,0) and is spanning in the (x,y) plane.
	
	# res_i: meters/hologram pixel. allows for rectangular pixels for 
	# different resolution in x and y.

	# wavelength: in meters
	
	
	#RANDOM=True # random initial phases for objects?
	#N_SA=10 # iterations until convergence is claimed
	#FRACTON_SA_BURN=0.71 #Burn-in phase lasts this fraction of N_SA iter's.
	
	# Method for quantizing hologram into black and white. See below.
	#METHOD='real' # 'real' or 'phase'. 
	
	# This turned out to be crucial for nice holograms. 
	# It takes into account the fact that pixels are ~ Gaussian. 
	# See holo_sum.pyx.
	#ATTENUATION=True 
	
	# If viewing spot from laser by placing hologram next to eye, one can 
	# take into account spot distance to hologram. Even if set to infty when 
	# in fact it is not there, eyeballs are flexible and can compensate :)
	# I don't think setting it to anything other than infty is very useful.
	# But may be wrong. So, left it here.
	# POINT_SOURCE_DISTANCE=1.e8 #if >1e7, then \equiv infty
	
	# Factor controlling the reduction in amplitude noise. 
	# For exact implementation, see its usage below.
	# AMPL_FLUCT=0.1
	
	n_objects=len(object_position_x)
	object_amplitude=np.ones(n_objects,dtype=np.complex128)
	object_amplitude=object_amplitude_in
	
	npix_x=int(holo_aperture_x/res_x+0.5)
	npix_y=int(holo_aperture_y/res_y+0.5)
	holo_position_x=np.array(range(npix_x),dtype=np.float64)*res_x-(res_x*(npix_x-1.0))/2.0
	holo_position_y=np.array(range(npix_y),dtype=np.float64)*res_y-(res_y*(npix_y-1.0))/2.0
	
	holo_position_x=np.repeat([holo_position_x],npix_y,axis=0).T
	holo_position_y=np.repeat([holo_position_y],npix_x,axis=0)
	
	print 'image inside a circle of diameter =',np.sqrt(object_position_x**2+object_position_y**2).max()*2,'m'
	

	
	objects=np.zeros(n_objects,dtype=np.complex128)
	objects_r=np.zeros(n_objects,dtype=np.float64)
	objects_i=np.zeros(n_objects,dtype=np.float64)
	
	holo=np.zeros((npix_x,npix_y),dtype=np.complex128)
	holo_r=np.zeros((npix_x*npix_y),dtype=np.float64)
	holo_i=np.zeros((npix_x*npix_y),dtype=np.float64)
	
	rphase=np.ones(n_objects,dtype=np.complex128)
	if (RANDOM):
		rphase=np.exp(2.j*np.pi*np.random.uniform(size=n_objects))
	
	att=0
	if (ATTENUATION):
		att=1
	
	
	# initialize
	objects=rphase
	
	
	std_old=0
	ind=0
	indd=0
	ampl_noise=1.
	while (ind<N_SA):
		phi_new=np.angle(objects)
		
		# Add random phases. Gradually reduce the amplitude of the random numbers. Somewhat resembling simulated annealing.
		if ((ind<int(N_SA*FRACTON_SA_BURN+0.5)) and (ind >0)):
			phi_new+=(np.random.uniform(size=(n_objects))-0.5)*2.0*np.pi/np.float64(ind+1)
		
		# Let us trace waves from the objects/sources to the plane of the hologram and let them interfere:
		transform_with_phase( object_position_x, object_position_y, object_position_z,
						holo_position_x.flatten(), holo_position_y.flatten(),
						np.real(object_amplitude*ampl_noise*np.exp(1.0j*phi_new)),
						np.imag(object_amplitude*ampl_noise*np.exp(1.0j*phi_new)),
						holo_r,holo_i,
						n_objects, npix_x*npix_y,
						att, POINT_SOURCE_DISTANCE, wavelength,res_x,res_y, 2)
		holo=holo_r.reshape((npix_x,npix_y))+1.0j*holo_i.reshape((npix_x,npix_y))
		
		# How do you reduce the hologram into black and white pixels? Picking a threshold in phase or in real values?
		if (METHOD=='phase'):
			psi_new=(mod(np.angle(holo)+np.pi,2.0*np.pi)<np.pi)*1.0
		if (METHOD=='real'):
			medi=np.median(np.real(holo))
			psi_new=(np.real(holo)>medi)*1.0
			
		if (N_SA==1):
			break
		
		# Let us reconstruct the sources by tracing the waves from the hologram to the source/object locations.
		# The brightness of the sources constituting the hologram is encoded in the (real) black-and-white image
		# given by the array psi_new.
		transform_with_phase( object_position_x, object_position_y, object_position_z,
						holo_position_x.flatten(), holo_position_y.flatten(),
						objects_r,objects_i,
						psi_new.flatten(),psi_new.flatten()*0.0,
						n_objects, npix_x*npix_y,
						att, POINT_SOURCE_DISTANCE, wavelength,res_x,res_y, 1)
		objects=objects_r+1.0j*objects_i
		
		#Below, we check whether the reconstructed amplitudes (i.e. brightness) of the input sources match the initial ones.
		reconstructed_amps=np.abs(objects)
		rats=reconstructed_amps/np.abs(object_amplitude)
		rats/=np.median(rats) # overall rescaling of all amplitudes is irrelevant
		std=rats.std()
		ampl_fluctuation=std*AMPL_FLUCT
		if (AMPL_FLUCT>0.0001): # Saturate amplitude noise, so that it doesn't become too large.
			rats[np.where(rats>1.0+ampl_fluctuation)]=1.0+ampl_fluctuation
			rats[np.where(rats<1.0-ampl_fluctuation)]=1.0-ampl_fluctuation
			ampl_noise=rats
		print 'it=',indd,'; std.dev. of reconstructed/initial ampl. = ',std
		if ((ind==N_SA-1)and (indd<N_SA+5)): 
			if (std_old<std): # if std increased in this iteration, make one additional iteration up to a max of extra 5
				ind=N_SA-2
		std_old=std
		ind+=1
		indd+=1
	return psi_new

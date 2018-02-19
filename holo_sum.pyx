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

import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sin, cos, acos, exp, sqrt, fabs, M_PI

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
@cython.embedsignature(True)
def transform_with_phase(np.ndarray[np.float64_t, ndim=1] object_position_x,
                         np.ndarray[np.float64_t, ndim=1] object_position_y,
                         np.ndarray[np.float64_t, ndim=1] object_position_z,
                         
                         np.ndarray[np.float64_t, ndim=1] holo_position_x,
                         np.ndarray[np.float64_t, ndim=1] holo_position_y,
                         
                         np.ndarray[np.float64_t, ndim=1] one_r, # real value of compnlex amplitude at object location
                         np.ndarray[np.float64_t, ndim=1] one_i, # imag ...
                         np.ndarray[np.float64_t, ndim=1] two_r, # real values of complex ampl at hologram location
                         np.ndarray[np.float64_t, ndim=1] two_i, # imag ...
                         
                         
                         np.int32_t n_objects,
                         np.int32_t npix,
                         
                         np.int32_t ATTENUATION,
                         
                         
                         np.float64_t POINT_SOURCE_DISTANCE,
                         np.float64_t wavelength,np.float64_t res_x,np.float64_t res_y,
                         np.int32_t DIR  
                 ):
    
    cdef int i, j, k
    cdef np.float64_t z_atten,dist,pi2,xk,yk,zk,xi,yj,distj,disti,distk,z_attenk,x
    cdef np.float64_t phase_r,phase_i,one_rk,one_ik, distTmp
    
    pi2=2.0*3.141592653589793238462643383279502884197169/wavelength #writing many digits of pi = soothing.

    
    from cython.parallel cimport prange,parallel
    cdef int nthreads
    from multiprocessing import cpu_count
    nthreads=cpu_count()
    #print 'nthreads = ',  nthreads
    
    if (DIR==1):
        one_r*=0.0
        one_i*=0.0
        pi2*=-1.0
    else:
        two_r*=0.0
        two_i*=0.0
        
    with nogil, parallel(num_threads=nthreads):
        for k in prange(n_objects,schedule='static',chunksize=n_objects//nthreads): 
            xk=object_position_x[k]
            yk=object_position_y[k]
            zk=object_position_z[k]
            distk=zk*zk
            z_atten=1.0
            for i in range(npix):
                xi=holo_position_x[i]
                yj=holo_position_y[i]
                disti=(xk-xi)*(xk-xi) 
                distj=(yk-yj)*(yk-yj) 
                dist=distk+disti+distj
                dist=sqrt(dist) 
                
                if (ATTENUATION):
                    x=pi2/zk
                    # This is gaussian attenuation, divided by distance. 
                    # The Gaussian gives pretty good image of the cube on transparent printer paper. 
                    # Slide-based holos look great with this attenuation turned on.
                    # Tried other types of attenuation but this seems to work best.
                    z_atten=(exp(-x*x*(disti*res_x*res_x+distj*res_y*res_y)/2.)+0.05)/zk #0.05 is the minimum attenuation. Somewhat randomly chosen,though 10x smaller gives too much noise far from center at 600dpi
                
                if (POINT_SOURCE_DISTANCE<100.):
                    distTmp=sqrt(POINT_SOURCE_DISTANCE**2+xi*xi+yj*yj)-POINT_SOURCE_DISTANCE
                    dist= dist + distTmp
                elif (POINT_SOURCE_DISTANCE<1.e7):
                    dist= dist + (xi*xi+yj*yj)/(2.*POINT_SOURCE_DISTANCE)
                
                dist=dist*pi2
                phase_r= cos(dist)
                phase_i= sin(dist)
                if (DIR==2): # send waves from source objects to hologram plane.
                    two_r[i]+=(phase_r*one_r[k]-phase_i*one_i[k])/z_atten
                    two_i[i]+=(phase_i*one_r[k]+phase_r*one_i[k])/z_atten
                else: # send waves from hologram to positions of hologram images. Inverse of above
                    one_r[k]+=( phase_r*two_r[i]+phase_i*two_i[i])*z_atten
                    one_i[k]+=(-phase_i*two_r[i]+phase_r*two_i[i])*z_atten

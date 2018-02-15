# 
# This file is part of pyHolo. 
# Copyright (C) 2015-2018  Svetlin Tassev
# 						 Braintree High School
#						 Harvard-Smithsonian Center for Astrophysics
# 
#    pyHolo is free software: you can redistribute it and/or modify
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
import matplotlib.pyplot as plt
from pyHolo import calculate_hologram

# Output resolution of hologram below in dpi. For printing on 
# transparencies, hopefully, your printer can support at least 
# 1200x600dpi. By that, I mean it should REALLY have that resolution. 
# This depends on drum age, transparency quality, etc. To make high 
# quality holograms, I display the image on my hi-res computer screen, 
# then take a picture of the screen in a dark room with film camera on 
# Iford PANF Plus 50 negative. Beware of optical resolution issues due to 
# bad lenses. I tested my objective lens resolution by first mounting it 
# on a digital camera, varying the focal length and f-stop. Optimal 
# f-number for my lens turned out to be around 9.5 ... that is if my 
# memory is not mistaken as I cannot find my notes on this ... Make sure 
# you use a solid tripod and the auto-timer and/or remote to reduce 
# vibrations when taking photos. The image should be displayed 1:1 on the
# screen, to avoid aliasing/interpolation issues from the viewer/screen.
# dpi=5000 also works well, but you start seeing artifacts with a red 
# laser, though not so much with green.

dpi_x=4000
dpi_y=4000

#Red laser wavelength. Green laser with same hologram is also great.
wavelength=650e-9

# holo_aperture_i is the physical size of the hologram in meters 
# These values are printed when running the code. Make sure the physical 
# hologram matches this size. If you are using Leika format negative, 
# take its physical size into account, and adjust distance to screen as 
# necessary. For instance, my monitor does not fill the whole slide when 
# producing a holo at 4000dpi.
holo_aperture_x=3840./dpi_x*0.0254 # 3840 is my hor. screen size in px
holo_aperture_y=2160./dpi_y*0.0254 # 2160 is my vert. screen size in px

#holo_aperture_x=0.036
#holo_aperture_y=0.024
holo_size_str='physical size of hologram in (x,y) = ('+str(holo_aperture_x)+', '+str(holo_aperture_y)+') meters'
print holo_size_str


res_x=0.0254/dpi_x
res_y=0.0254/dpi_y

object_amplitude,object_position_x, object_position_y, object_position_z=np.loadtxt('input.dat').T

hologram=calculate_hologram(object_amplitude,object_position_x, object_position_y, object_position_z,
	holo_aperture_x,holo_aperture_y,res_x,res_y,wavelength)


fig=plt.figure()
ax=plt.imshow(hologram.T,cmap='Greys_r',interpolation='nearest',origin='lower')	
plt.axis('off')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
plt.show()
#If saving, make sure that output image has the same EXACT pixel size as psi_new array.
#Also, make sure you are not using compression for the output image. It will probably spoil the hologram.

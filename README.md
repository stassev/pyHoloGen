**Author:** Svetlin V. Tassev (Braintree High School, Harvard-Smithsonian Center for Astrophysics)

**Initial public release date:** Feb 14,2018

pyHolo is a multithreaded Python/Cython code for calculating computer-generated binary holograms (CGH).

I wrote the code to produce diffraction demonstrations for my physics classes. Therefore, do not expect the code to be fast. However, I did spend time to optimize the attenuation function (in holo_sum.pyx), so that the holograms that are produced are usable when printed on transparencies with a 1200x600dpi printer: indeed, the quality of the holographic image (especially, when printing at low dpi) can be improved quite a lot by playing with that function. I usually print the holograms, covering the full letter format; thus, one can look through the hologram with both eyes, taking advantage of depth perception. I have also successfully transferred the holograms to slides at resolutions of up to 5000dpi. To do that, I just take a photo with a film camera of the generated hologram image as it is shown on my laptop screen. An ISO-50 black and white film works well. I have included some more suggestions in the code itself.

If you use pyHolo for educational purposes or just for fun, I'd appreciate it if you send me a note, example files, video of a hologram in action, etc. I'd be more than happy to add your examples as a resource in the downloads section with proper attribution.

* pyHolo is free and open-source software, distributed under the GPLv3 license.

* To build the code, you need to run:
  

```
#!bash

  python2 setup.py build_ext --inplace
```


* To compile successfully, you need to have the following packages installed: [Python 2.7](https://www.python.org/), [Cython](http://cython.org/), [NumPy](http://www.numpy.org/), as well as their respective dependencies. 

* An example input.dat file is included along with example.py which produces a hologram image file, which is also available in the downloads section. There you can find a video of the hologram in action. The input dat file contains 4 columns: object brightness, x,y,z coordinates in meters. The hologram plane is at z=0. To run the example file just type:

```
#!bash

  python2 example.py
```


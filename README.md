**Author:** Svetlin V. Tassev (Braintree High School, Harvard-Smithsonian Center for Astrophysics)

**Initial public release date:** Feb 14,2018

pyHolo is a multithreaded Python/Cython code for calculating computer-generated binary holograms.

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


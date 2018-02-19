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

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.extension import Extension
from distutils.util import get_platform
from distutils.ccompiler import get_default_compiler

import os

try:
    from Cython.Distutils import build_ext as build_ext


    sources = [os.path.join(os.getcwd(), 'holo_sum.pyx')
    ]
except ImportError as e:
    sources = [os.path.join(os.getcwd(), 'holo_sum.c')
    ]
    for i in sources:
        if not os.path.exists(i):
            print i
            print os.path.exists(i)
            raise ImportError(str(e) + '. ' +
                'Cython is required to build the initial .c file.')

    # We can't cythonize, but that's ok as it's been done already.
    from distutils.command.build_ext import build_ext



include_dirs = []
library_dirs = []
package_data = {}

libraries = [] 


ext_modules = [Extension(
    "holo_sum",
    [sources[0]],
    extra_compile_args=['-fopenmp','-O3','-shared' ,'-pthread' ,'-fPIC' ,'-fwrapv','-fno-strict-aliasing'],
    extra_link_args=['-fopenmp','-O3','-shared' ,'-pthread' ,'-fPIC' ,'-fwrapv','-fno-strict-aliasing'],
    libraries=libraries,
    include_dirs=include_dirs
)
]

long_description="""Hologram maker
"""


setup_args = {
        'name': 'pyHoloGen',
        'version': 1.0,
        'author': 'Svetlin Tassev',
        'author_email': 'stassev@alum.mit.edu',
        'description': 'A Python/Cython code for calculating computer-generated binary holograms.',
        'url': '',
        'long_description': long_description,
        'classifiers': [
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Cython',
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Intended Audience :: Education',
            'Topic :: Education',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Physics'
            ],
        'packages':['pyHoloGen'],
        'ext_modules': ext_modules,
        'include_dirs': include_dirs,
        'cmdclass' : {'build_ext': build_ext},
  }



if __name__ == '__main__':
    setup(**setup_args)

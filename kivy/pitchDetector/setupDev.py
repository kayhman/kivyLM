from distutils.core import setup
from Cython.Build import cythonize

setup(name='autocorrelation',
      version='1.0',
      ext_modules = cythonize("autocorrelation/autocorrelation.pyx")
      )

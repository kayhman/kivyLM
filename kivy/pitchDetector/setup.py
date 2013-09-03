from distutils.core import setup
from distutils.extension import Extension

setup(name='autocorrelation',
      version='1.1',
      ext_modules =  [Extension("autocorrelation", ["autocorrelation/autocorrelation.c", "autocorrelation/autocorrelationOpt.c"])]
      )

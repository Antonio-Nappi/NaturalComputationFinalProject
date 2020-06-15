from distutils.core import setup
from Cython.Build import cythonize
setup(
    name='test app',
    ext_modules = cythonize('evolve_parameters.pyx'),
    zip_safe=False)
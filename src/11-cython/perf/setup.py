from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("math_core.pyx", language_level="3")
)

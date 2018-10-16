from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'Light-Up Tanner Wendland',
    ext_modules = cythonize(["src/*.pyx"], build_dir="build")
)

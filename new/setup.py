from distutils.core import setup
from distutils.extension import Extension
#from setuptools import setup, find_packages
from Cython.Build import cythonize

ext_modules = [
    Extension(
        r'centroid',
        [r'centroid.pyx',],
        extra_compile_args = ['-fopenmp',],
        extra_link_args    = ['-lgomp',],
        define_macros      = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
    ),
    Extension(
        r'is_balanced',
        [r'is_balanced.pyx',],
        extra_compile_args = ['-fopenmp',],
        extra_link_args    = ['-lgomp',],
        define_macros      = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
    ),
    Extension(
        r'polygon',
        [r'polygon.pyx',],
        extra_compile_args = ['-fopenmp',],
        extra_link_args    = ['-lgomp',],
        define_macros      = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
    ),
    Extension(
        r'is_balanced2',
        [r'is_balanced2.pyx',],
        extra_compile_args = ['-fopenmp',],
        extra_link_args    = ['-lgomp',],
        define_macros      = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
    ),
    Extension(
        r'cache',
        [r'cache.pyx',],
        extra_compile_args = ['-fopenmp',],
        extra_link_args    = ['-lgomp',],
        define_macros      = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
    ),
#    Extension(
#        r'polygons',
#        [r'polygons.pyx',],
#        extra_compile_args = ['-fopenmp',],
#        extra_link_args    = ['-lgomp',],
#        define_macros      = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
#    ),
]

setup(
    name='code-05',
    ext_modules=cythonize(ext_modules),
    #packages=['centroid',],
    package_data={'': ['*.pxd', '*.pyx',]}
)

from Cython.Compiler import Options
Options.embed = 'main'
cythonize('main.pyx')


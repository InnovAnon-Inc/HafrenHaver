#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

#cimport mpi4py
#from mpi4py     import MPI
#from mpi4py_map import map
from joblib     import Memory

cdef char*  cachedir = 'cache'
#cdef object mem      = Memory(cachedir, verbose=0)
cdef object mem      = Memory(cachedir)


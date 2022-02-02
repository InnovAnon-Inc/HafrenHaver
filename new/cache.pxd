#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

#cimport mpi4py
#from mpi4py      import MPI
#from mpi4py_map  import map

cdef public char*  cachedir
cdef public object mem


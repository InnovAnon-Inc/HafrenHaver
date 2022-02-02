#! /usr/bin/env -S cython3 --embed
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

cimport mpi4py
from mpi4py     import MPI
#from mpi4py_map import map

from is_balanced2 cimport is_balanced2
#from polygons     cimport polygon_helper
from polygons      import polygon_helper

cdef object comm = MPI.COMM_WORLD
cdef int    rank = comm.Get_rank()
cdef int    size = comm.Get_size()
print("Hello World from rank %s of %s" % (rank, size))

from fractions import Fraction
if rank == 0 and __name__ == '__main__':
	#s1 = (3, 4, 5,)
	#s2 = np.array(s1, dtype=np.intc)
	#print("fuck s2: %s" % (s2,), flush=True)
	#c = is_balanced2(s2, 7)
	#print("c: %s" % (c,))
	b  = 12
	nv =  7
	p  = polygon_helper(b, nv)
	print("p: %s" % (p,), flush=True)


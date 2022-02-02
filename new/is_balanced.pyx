#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

from centroid cimport centroid

cdef inline bint is_balanced(cy.double[:,::1] p):
#cdef bint is_balanced(cy.double[::1,:] p):
	cdef double[:] c = centroid(p)
	cdef double[:] o = np.ones(c.size, dtype=np.float)
	c = np.add(c, 1)
	return np.allclose(c, o)


#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

cdef inline cy.double[:,::1] polygon(cy.double[:] r):
#cdef cy.double[::1,:] polygon(cy.double[:] r):
	cdef double[:]     x   = np.cos(r)
	cdef double[:]     y   = np.sin(r)
	cdef double[::1,:] xy1 = np.array((x, y,), order='F')
	cdef double[:,::1] xy2 = xy1.T
	return xy2


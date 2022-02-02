#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

from libc.math   cimport M_PI

from is_balanced cimport is_balanced
from polygon     cimport polygon

cdef inline bint is_balanced2(cy.int[:] num, cy.int den):
	cdef double        a = 2 * M_PI / den
	cdef double[:]     b = np.multiply(num, a)
	cdef double[:,::1] c = polygon(b)
	return is_balanced(c)


#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

cdef public bint is_balanced(cy.double[:,::1] p)
#cdef public bint is_balanced(cy.double[::1,:] p)


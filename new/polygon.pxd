#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

cdef cy.double[:,::1] polygon(cy.double[:] r)


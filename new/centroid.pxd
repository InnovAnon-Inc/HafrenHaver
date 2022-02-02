#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

cdef public cy.double[:] centroid(cy.double[:,::1] vertexes)
#cdef public cy.double[:] centroid(cy.double[::1,:] vertexes)


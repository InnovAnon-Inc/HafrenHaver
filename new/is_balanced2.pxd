#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy  as cp
import  numpy  as np

#cdef struct s_pt:
#	cy.double x
#	cy.double y
#cdef public void rad_to_cart(s_pt* ret, cy.double rad) nogil

#cdef public cy.double[:] rat_to_rad(cy.int[:] num, cy.int den)

cdef public bint is_balanced2 (cy.int[:] p, cy.int den)


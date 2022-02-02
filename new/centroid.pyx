#! /usr/bin/env cython3
#cython: language_level=3

cimport cython as cy
cimport numpy as cp
import  numpy as np

from shapely.geometry import Polygon

cdef inline cy.double[:] centroid(cy.double[:,::1] vertexes):
#cdef inline cy.double[:] centroid(cy.double[::1,:] vertexes):
	cdef object    p1 = Polygon(vertexes) # Polygon
	cdef object    p2 = p1.centroid       # Point
	cdef object    p3 = p2.coords         # CoordinateSequence
	cdef double[:] p4 = np.array(p3).ravel()
	return p4
	#p3 = p3.xy
	#return p3[0]
	#return p3
	#return np.asarray(p3)


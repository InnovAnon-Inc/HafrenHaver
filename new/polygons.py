#! /usr/bin/env python3

from itertools       import product, chain, starmap, takewhile, combinations, accumulate, combinations_with_replacement, permutations
from functools       import reduce, cache, lru_cache
#from peval           import pure, inline, partial_apply
from typing          import Optional, Callable
from operator        import __or__, __and__, __sub__
from sympy           import divisors
from joblib import Memory
from math            import log, gcd, pi, cos, sin, isclose

from shapely.geometry import Polygon

import numba as nb
import numpy as np

cachedir = 'cache'
mem      = Memory(cachedir, verbose=0)

def polygon_helper1(r:list[list[list[int]]])->list[list[int]]: return tuple(chain.from_iterable(r))
def polygon_helper_kernel(beats:int, nvertex:int, offset:int, f:Callable[[int,int,int],list[list[int]]])->list[list[int]]:
    #print("polygon_helper_kernel(beats=%s, nvertex=%s, offset=%s)" % (beats, nvertex, offset,), flush=True)
    base = ((offset,),)
    if nvertex == 1: return base
    offs = range(offset+1, beats-(nvertex-1)+1)
    ret1 = map(f, offs)
    ret2 = chain.from_iterable(ret1)
    ret3 = product(base, ret2)
    ret4 = map(polygon_helper1, ret3)
    ret5 = tuple(ret4)
    #assert len(ret5) != 0
    return ret5
def polygon_helper_impl0(g:Callable[[Callable,int,int,int],list[list[int]]], beats:int, nvertex:int, offset:int)->list[list[int]]:
    #print("polygon_helper_impl0(beats=%s, nvertex=%s, offset=%s)" % (beats, nvertex, offset,), flush=True)
    f = lambda off: g(g, beats, nvertex-1, off)
    return polygon_helper_kernel(beats, nvertex, offset, f)
polygon_helper_impl = mem.cache(polygon_helper_impl0)
def polygon_helper(beats, nvertex):
    #print("polygon_helper(beats=%s, nvertex=%s)" % (beats, nvertex,), flush=True)
    return polygon_helper_impl(polygon_helper_impl, beats, nvertex, 0)

def centroid(vertexes)->list[float]:
    #print("centroid(vertexes=%s)" % (vertexes,), flush=True)
    p1 = Polygon(vertexes) # Polygon
    p2 = p1.centroid       # Point
    p3 = p2.coords         # CoordinateSequence
    p4 = np.array(p3).ravel()
    return p4
def is_balanced(p:list[list[float]]):
    #print("is_balanced(p=%s)" % (p,), flush=True)
    c = centroid(p)
    o = np.ones(c.size, dtype=np.float)
    c = np.add(c, 1)
    return np.allclose(c, o)
def polygon(r:list[float])->list[tuple[float,float]]:
    #print("polygon(r=%s)" % (r,), flush=True)
    x   = tuple(map(cos, r))
    y   = tuple(map(sin, r))
    xy1 = (x, y)
    xy2 = tuple(zip(*xy1))
    #xy1 = np.array((x, y,), order='F')
    #xy2 = xy1.T
    return xy2
def is_balanced2(num:list[int], den:int)->bool:
    #print("is_balanced2(num=%s, den=%s)" % (num, den,), flush=True)
    a = 2 * pi / den
    f = lambda k: k*a
    b = tuple(map(f, num))
    c = polygon(b)
    return is_balanced(c)
def balanced_polygons(beats):
    #print("balanced_polygons(beats=%s)" % (beats,), flush=True)
    nv = range(3, beats+1)
    f  = lambda k: polygon_helper(beats, k)
    p  = map(f, nv)
    q  = chain.from_iterable(p)
    g  = lambda k: is_balanced2(k, beats)
    r  = tuple(filter(g, q))
    return r

def balanced_polygons2(m):
    n = range(m+1)
    f = lambda k: (balanced_polygons(k), k)
    p = map(f, n)
    #q = chain.from_iterable(p)
    #r = tuple(q)
    return p

if __name__ == '__main__':
    n = 30
    p = balanced_polygons2(n)
    #print()
    for a, b in p:
        print("b: %s" % (b,), flush=True)
        for c in a:
            print("c: %s" % (c,), flush=True)
        print()
    print()


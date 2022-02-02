#! /usr/bin/env python3

from itertools       import product, chain, starmap, takewhile, combinations, accumulate, combinations_with_replacement, permutations
from functools       import reduce, cache, lru_cache
#from peval           import pure, inline, partial_apply
from typing          import Optional, Callable
from operator        import __or__, __and__, __sub__
from sympy           import divisors
from joblib import Memory

import numba as nb

cachedir = 'cache'
mem      = Memory(cachedir)

def polygon_helper1(r:list[list[list[int]]])->list[list[int]]: return tuple(chain.from_iterable(r))
def polygon_helper_kernel(beats:int, nvertex:int, offset:int, f:Callable[[int,int,int],list[list[int]]])->list[list[int]]:
    print("polygon_helper_kernel(beats=%s, nvertex=%s, offset=%s)" % (beats, nvertex, offset,), flush=True)
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
    print("polygon_helper_impl0(beats=%s, nvertex=%s, offset=%s)" % (beats, nvertex, offset,), flush=True)
    f = lambda off: g(g, beats, nvertex-1, off)
    return polygon_helper_kernel(beats, nvertex, offset, f)
polygon_helper_impl = mem.cache(polygon_helper_impl0)
def polygon_helper(beats, nvertex):
    print("polygon_helper(beats=%s, nvertex=%s)" % (beats, nvertex,), flush=True)
    return polygon_helper_impl(polygon_helper_impl, beats, nvertex, 0)


if __name__ == '__main__':
    n = 30
    r = range(3, n+1)
    f = lambda k: polygon_helper(n, k)
    p = tuple(map(f, r))
    print()
    for a in p:
        for b in a:
            print("b: %s" % (b,), flush=True)
        print()
    print()


#! /usr/bin/env cython3
#cython: language_level=3

from enum            import Enum, unique
from ordered_enum    import OrderedEnum
from fractions       import Fraction
from geopy.geocoders import Nominatim
from pathlib         import Path
from ephem           import Observer, Sun, city
from datetime        import datetime
from math            import log, gcd, pi, cos, sin, isclose
from bjorklund       import bjorklund
from itertools       import product, chain, starmap, takewhile, combinations, accumulate, combinations_with_replacement, permutations
from ast             import literal_eval as make_tuple
#from functools       import cache, reduce, lru_cache
from functools       import reduce
from random          import choice, randrange
from peval           import pure, inline, partial_apply
from typing          import Optional, Callable
#from strict_hint     import strict
from numbers         import Number
#from persistent_lru_cache import persistent_lru_cache
#from keepit          import keepit
from operator        import __or__, __and__, __sub__
from sys             import float_info
#from factors    import nfact
from sympy           import divisors
from mpi4py import MPI
from joblib import Memory
from statistics import mean
from shapely.geometry import Polygon

from numba import jit
import numba as nb

from mpi4py_map import map

#from mpi4py_map import map
from cache import mem
from const import BrainWaves, RATIOS
from freq  import interpolate, base_frequency
from astro import get_gps_hz_adjustment, timeofday

###@strict
#@inline
def limit()->int: return choice((3, 5, 7, 17,)) # TODO

#@strict
#@inline
def scale(L:int)->list[Fraction]: return (Fraction(1, 1), *choice(RATIOS[L]))


#@strict
#@inline
#@pure
def brainrange(T:tuple[bool,float,int])->BrainWaves:
    day, hour, length = T
    hour = int(hour)
    if day:
        if hour ==  0: return BrainWaves.EPSILON
        if hour ==  1: return BrainWaves.BETA
        if hour ==  2: return BrainWaves.ALPHA
        if hour ==  3: return BrainWaves.BETA
        if hour ==  4: return BrainWaves.THETA
        if hour ==  5: return BrainWaves.BETA
        if hour ==  6: return BrainWaves.ALPHA
        if hour ==  7: return BrainWaves.BETA
        if hour ==  8: return BrainWaves.THETA
        if hour ==  9: return BrainWaves.BETA
        if hour == 10: return BrainWaves.ALPHA
        if hour == 11: return BrainWaves.EPSILON
    else:
        if hour ==  0: return BrainWaves.EPSILON
        if hour ==  1: return BrainWaves.BETA
        if hour ==  2: return BrainWaves.BETA
        if hour ==  3: return BrainWaves.ALPHA
        if hour ==  4: return BrainWaves.THETA
        if hour ==  5: return BrainWaves.DELTA
        if hour ==  6: return BrainWaves.THETA
        if hour ==  7: return BrainWaves.ALPHA
        if hour ==  8: return BrainWaves.THETA
        if hour ==  9: return BrainWaves.DELTA
        if hour == 10: return BrainWaves.THETA
        if hour == 11: return BrainWaves.EPSILON
    # TODO make these properties of the brainwaves?
    raise Exception()
#@strict
#@inline
def brainwave(B:Number, s:list[Fraction], R:tuple[float,float])->tuple[int,int]: return choice(interpolate(B, s, R))

@unique
class SongType(Enum):
    PHRASE    = (      7,       9)
    VERSE    = (      8,      16)
    POP      = (     60,     120)
    ROCK     = (     60,     900)
    SYMPHONY = (1*60*60, 4*60*60)
#@strict
#@inline
def songtype()->tuple[int,int]: return choice(tuple(SongType)).value
#@strict
#@inline
#@pure
# TODO
#@jit
def beats(B:float, s:list[Fraction], f:tuple[int,int], t:tuple[int,int])->tuple[int,int]:
    # B: base freq, s: scale, f: (degree, octave), t: song type time range
    print("f: %s" % (f,))
    print("s: %s" % (s,))
    f  = B * s[f[0]] * 2**f[1]
    print("f: %s" % (f,))
    #d  = 1 / f
    #print("d: %s" % (d,))
    #dl = int(t[0] / d)
    #du = int(t[1] / d)
    dl = int(t[0]*f)
    du = int(t[1]*f)
    #return randrange(dl, du+1)
    return dl,du

###@strict
#@inline
#@pure
# TODO
#@jit
def rat_to_rad(rat:Number)->float: return 2*pi*rat
#@strict
#@inline
#@pure
# TODO
#@jit
def rad_to_cart(rad:Number)->tuple[float,float]: return (cos(rad), sin(rad))

#@inline
#@pure
# TODO
#@jit(nb.boolean(nb.float32,nb.float32))
#@jit
def isclose2(a:float, b:float)->bool: return isclose(a, b, abs_tol=float_info.min)

#@keepit('iscloses.tsv') # disk space
#@inline
#@pure
# TODO
#@jit
def iscloses(t1:tuple[tuple[float,float]], t2:tuple[tuple[float,float]])->bool:
    t3 = zip(t1, t2)
    #t = tuple(t)
    #print("iscloses t1: %s" % (t,))
    t4 = starmap(isclose2, t3)
    #t = tuple(t)
    #print("iscloses t2: %s" % (t,))
    t5 = reduce(__and__, t4)
    #print("iscloses t3: %s" % (t,))
    return t5
# TODO
#iscloses1 = partial_apply(iscloses, (1, 1,))
#@inline
#@pure
@jit
def inc(n:float)->float: return n + 1.0
#@strict
#@keepit('balanced_helper.tsv') # disk space
#@inline
#@pure
@jit
def balanced_helper(p:list[Number])->bool:
    p1 = map(rat_to_rad,  p)

    #p = tuple(p)

    p2 = map(rad_to_cart, p1)
    p3 = tuple(p2)
    p4 = centroid(p3)
    #p = p == (0, 0) # TODO floating point equality
    p5 = map(inc, p4)
    #p = (p[0]+1, p[1]+1)
    p6 = iscloses(p5, (1, 1,))
    # TODO
    #p = iscloses1(p)
    #p = iscloses(p, (0, 0,))
    #if p: print("balanced polygon: %s" % (polygon,))
    return p6

outfile = open("%s.out" % (__file__,), 'w')
##@strict
##@inline
#@pure
#def balanced(beats:int, polygon:list[int])->bool:
#    #print("balanced(beats=%s, polygon=%s" % (beats, polygon,))
#    p = map(lambda v: Fraction(v,beats),          polygon)
#    #p = tuple(p) # TODO tuple unnecessary
#
#    #p = tuple(p)
#
#    p = balanced_helper(p)
#    #print("len(%s): %s" % (polygon, len(polygon)))
#    assert len(polygon) != 0
#    assert len(polygon) != beats or p
##    #print("balanced p1: %s" % (p,))
##    #p = map(lambda k: 2*pi*k,           p)
##    p = map(rat_to_rad,           p)
##    p = tuple(p)
##    #print("balanced p2: %s" % (p,))
##    #p = map(lambda r: (cos(r), sin(r)), p)
##    p = map(rad_to_cart, p)
##    p = tuple(p)
##    #print("balanced p3: %s" % (p,))
##    p = centroid(p)
##    #print("balanced p4: %s" % (p,))
##    p = p == (0, 0) # TODO floating point equality
#    if p: print("balanced polygon: %s %s" % (beats, polygon,), file=outfile, flush=True)
#    return p
#
# TODO
#@keepit('balanced2.tsv')
#@inline
#@pure
# TODO
#@jit
def balanced2(f:Callable[[int],float], polygon:list[int])->bool:
    #print("balanced2(f=%s, polygon=(%s) %s)" % (f, type(polygon), polygon,))
    p1 = map(f,          polygon)
    #p = balanced_helper(p)
    p2 = map(rat_to_rad,  p1)
    p3 = map(rad_to_cart, p2)
    p4 = tuple(p3)
    p5 = centroid(p4)
    p6 = map(inc, p5)
    # TODO
    #p = iscloses1(p)
    p7 = iscloses(p6, (1, 1,))
    assert len(polygon) != 0
    #assert len(polygon) != beats or p
    #if p: print("balanced polygon: %s %s" % (beats, polygon,), file=outfile, flush=True)
    return p7

#@strict
#@cache # ?
#@inline
#@pure
#def polygon_helper1(r:list[list[list[int]]])->list[list[int]]: return tuple(chain(*r))
# TODO
#@jit
def polygon_helper1(r:list[list[list[int]]])->list[list[int]]: return tuple(chain.from_iterable(r))
#@inline
#@pure
@jit
def polygon_helper2(r:list[list[int]])->list[list[int]]: return tuple(map(tuple, r))
# TODO is okay ???
#def polygon_helper1(r:list[list[list[int]]])->list[list[int]]: return chain(*r)
#@strict
#@cache # ?
#@keepit('polygon_helper0.tsv')
#@inline
#@pure
#def polygon_helper0(ret:list[list[int]], offset:int)->list[list[int]]:
#    base = ((offset,),)
#    #ret  = chain(*ret)
#    #ret  = tuple(ret)
#    ret = polygon_helper1(ret)
#    #print("a: %s" % (type(ret),))
#    ret  = product(base, ret)
#    #print("b: %s" % (type(ret),))
#    #f    = lambda r: tuple(chain(*r))
#    #ret  = map(f, ret)
#    ret  = map(polygon_helper1, ret)
#    #print("c: %s" % (type(ret),))
#    ret  = tuple(ret)
#    #ret = polygon_helper2(ret)
#    #print("d: %s" % (type(ret),))
#    assert len(ret) != 0
#    return ret



#@keepit('polygon_helper_kernel.tsv')
#@lru_cache
#@inline
#@pure
# TODO
#@jit
def polygon_helper_kernel(beats:int, nvertex:int, offset:int, f:Callable[[int,int,int],list[list[int]]])->list[list[int]]:
    base = ((offset,),)
    if nvertex == 1: return base
    offs = range(offset+1, beats-(nvertex-1)+1)
    #offs = tuple(offs)

    #offs = tuple(offs)

    #f    = lambda off: polygon_helper(beats, nvertex-1, off)
    ret1  = map(f, offs)
    #ret = polygon_helper2(ret)
    #ret = map(tuple, ret)
    #ret  = polygon_helper0(ret, offset)
    #ret = polygon_helper1(ret)
    #ret = chain(*ret)
    ret2 = chain.from_iterable(ret1)
    #print("a: %s" % (type(ret),))
    ret3  = product(base, ret2)
    #print("b: %s" % (type(ret),))
    #f    = lambda r: tuple(chain(*r))
    #ret  = map(f, ret)
    ret4  = map(polygon_helper1, ret3)
    #print("c: %s" % (type(ret),))
    ret5  = tuple(ret4)
    #ret = polygon_helper2(ret)
    #print("d: %s %s" % (type(ret), ret))
    assert len(ret5) != 0
    return ret5
#polygon_helper_kernel = mem.cache(polygon_helper_kernel_impl)
#    ret  = chain(*ret)
#    ret  = tuple(ret)
#    ret  = product(base, ret)



#Func<Func<Double, Double>, Func<Double, Double>> fact =
#  (recurs) =>
#    (x) =>
#      x == 0 ? 1 : x * recurs(x - 1);
#
#def polygon_helper0(recurs:Callable[[int,int,int],list[list[int]]])->Callable[[int,int,int],list[list[int]]]:
#@lru_cache
#@inline
#@pure
#def polygon_helper0(g:Callable[[Callable,int,int,int],list[list[int]]], beats:int, nvertex:int)->Callable[[int],list[list[int]]]:
#    return lambda off: g(g, beats, nvertex, off)
    #return partial_apply(polygon_helper, beats, nvertex)
#polygon_helper0 = mem.cache(polygon_helper0_impl)

#@strict
#@cache
#@cache_to_disk(99)
#@disk_cache
#@keepit('polygon_helper.tsv')
#@inline
#@pure
# TODO
#@jit
def polygon_helper_impl0(g:Callable[[Callable,int,int,int],list[list[int]]], beats:int, nvertex:int, offset:int)->list[list[int]]:
    #f    = lambda off: polygon_helper(beats, nvertex-1, off)
    #f = polygon_helper0(g, beats, nvertex-1)
    f    = lambda off: g(g, beats, nvertex-1, off)
    #f = partial_apply(polygon_helper, beats, nvertex-1)
    return polygon_helper_kernel(beats, nvertex, offset, f)
#polygon_helper_impl = partial_apply(polygon_helper_impl0, polygon_helper_impl0)
polygon_helper_impl = lambda beats, nvertex, offset: polygon_helper_impl0(polygon_helper_impl0, beats, nvertex, offset)
polygon_helper = mem.cache(polygon_helper_impl)
#    base = ((offset,),)
#    if nvertex == 1: return base
#    offs = range(offset+1, beats-(nvertex-1)+1)
#    #offs = tuple(offs)
#
#    #offs = tuple(offs)
#
#    f    = lambda off: polygon_helper(beats, nvertex-1, off)
#    ret  = map(f, offs)
#    #ret = polygon_helper2(ret)
#    #ret = map(tuple, ret)
#    #ret  = polygon_helper0(ret, offset)
#    #ret = polygon_helper1(ret)
#    ret = chain(*ret)
#    #print("a: %s" % (type(ret),))
#    ret  = product(base, ret)
#    #print("b: %s" % (type(ret),))
#    #f    = lambda r: tuple(chain(*r))
#    #ret  = map(f, ret)
#    ret  = map(polygon_helper1, ret)
#    #print("c: %s" % (type(ret),))
#    ret  = tuple(ret)
#    #ret = polygon_helper2(ret)
#    #print("d: %s %s" % (type(ret), ret))
#    assert len(ret) != 0
#    return ret
##    ret  = chain(*ret)
##    ret  = tuple(ret)
##    ret  = product(base, ret)
##    f    = lambda r: tuple(chain(*r))
##    ret  = map(f, ret)
#    ret  = tuple(ret)
#    return ret

#@inline
#@pure
#@jit
def congruent(beats:int, p:list[int])->bool:
    p1 = (*p[1:], beats)
    p2 = gcd(*p1)
    return p2 == 1

#@strict
#@cache
#@cache_to_disk(99)
#@disk_cache
# TODO
#@keepit('balanced_polygon_helper.tsv')
#@inline
#@pure
#@jit
def balanced_polygon_helper(beats:int, nv:int)->list[list[int]]:
    ret1 = polygon_helper(beats, nv, 0)
    g1   = lambda p: congruent(beats, p)
    ret2 = filter(g1, ret1) # filter out polygons which are congruent to those already tested
    #print("balanced_polygon_helper ret: (%s) %s" % (type(ret), ret,))
    #f   = lambda p: balanced(beats, p)
    #g   = partial_apply(Fraction, den=beats)
    g2   = lambda v: Fraction(v, beats)
    #f   = partial_apply(balanced2, g)
    f   = lambda p: balanced2(g2, p)
    ret3 = filter(f, ret2)
    ret4 = tuple(ret3)
    #if len(ret) != 0:
    #ret = tuple(map(tuple,ret))
    for k in ret4: print("balanced_polygon_helper ret: %2s/%2s %s" % (len(k), beats, k,), file=outfile, flush=True)
    return ret4

#@inline
#@pure
#@jit
def rotation(a:list[int], k:int)->list[int]: return (*a[k:], *a[:k])
#@lru_cache
#@inline
#@pure
#@jit
#def rotation_a(a:list)->Callable[[int,],list]: return partial_apply(rotation, a)
def rotation_a(a:list)->Callable[[int,],list]: return lambda k: rotation(a, k)

#@keepit('rotations')
#@inline
#@pure
#@jit
def rotations_impl(a:list[int])->list[int]:
    ret1 = range(len(a))
    #f   = lambda k: (*a[k:], *a[:k])
    f = rotation_a(a)
    ret2 = map(f, ret1)

    ret3 = set(ret2)
    ret4 = tuple(ret3)

    return ret4 # we could return a map
rotations = mem.cache(rotations_impl)
##@inline
##@keepit('rotated_polygon_helper0')
#@pure
#def rotated_polygon_helper0(a:list[int], b:list[int])->bool:
#    #a = tuple(a)
#    b = tuple(b)
#    #print("rotated_polygon_helper0(a=%s, b=%s)" % (a, b,))
#    a = rotations(a)
#    #a = tuple(a)
#    f = lambda r: r != b
#    c = takewhile(f, a)
#    return len(a) == len(c)
#@inline
#@pure
#@jit
def inv_accumulate(a:list[int])->list[int]:
    a1 = tuple(a)
    #a = starmap(__sub__, izip(a[1:], a))
    a2 = zip(a1[1:], a1)
    a3 = starmap(__sub__, a2)
    a4 = tuple(a3)
    return a4
#@inline
#@pure
#@jit
def inv_accumulate2(beats:int, a:list[int])->list[int]:
    b1 = inv_accumulate(a)
    b2 = (*b1, beats-a[-1])
    return b2
#@inline
#@pure
@jit
def inv_accumulate3(a:list[int])->list[int]:
    a1 = (0, *a)
    b1 = inv_accumulate(a1)
    return b1
##@inline
#@pure
#def product3(A:list[int], a:int)->list[int,int]:
#    ret = range(a+1, len(A))
#    f   = lambda i: (A[a], A[i])
#    ret = map(f, ret)
#    return ret
##@inline
#@pure
#def product2(A:list[int])->list[int,int]:
#    f   = lambda k: product3(A, k)
#    ret = range(len(A))
#    ret = map(f, ret)
#    ret = chain.from_iterable(ret)
#    ret = chain(A, ret)
#    return ret
#@inline
#@pure
#@jit
def accumulate2(k:list[int])->list[int]:
    k1 = accumulate(k)
    k2 = tuple(k1)
    k3 = (0, *k2[:-1])
    return k3
# TODO
#@keepit('rotated_polygon_helper')
#@inline
#@pure
def rotated_polygon_helper(beats:int, nv:int)->list[list[int]]:
    print("rotated_polygon_helper(beats=%s, nv=%s)" % (beats, nv,))
    ret = balanced_polygon_helper(beats, nv)
    print("rotated polygon helper ret 1: %s" % (ret,))
    #ret = map(inv_accumulate, ret)
    f   = lambda k: inv_accumulate2(beats, k)
    ret = map(f, ret)
    ret = tuple(ret) #
    print("rotated polygon helper ret 2: %s" % (ret,))
    #ret = combinations(ret, 2)
    #ret = product2(ret)
    #ret = tuple(ret) #
    #print("rotated polygon helper ret 3: %s" % (ret,))
    #ret = filter(rotated_polygon_helper0, ret)
    tmp = []
    f   = lambda k: ret[k]
    # TODO
    for a in range(len(ret)):
        flag = True
        R    = rotations(ret[a])
        b    = range(a+1, len(ret))
        b    = map(f, b)
        for k, m in product(R, b):
            if k == m:
                flag = False
                break
        if flag: tmp.append(ret[a])
    ret = tmp
    #ret = tuple(ret) #
    #print("rotated polygon helper ret 4: %s" % (ret,))
    #ret = map(accumulate, ret)
    ret = map(accumulate2, ret)
    #ret = map(tuple, ret)
    ret = tuple(ret)
    #assert len(ret) != 0
    if len(ret) != 0:
        for k in ret: print("rotated polygon helper ret 5: %2s/%2s %s" % (nv, beats, k,), file=outfile, flush=True)
    return ret

###@strict
#@cache
#@inline
#@pure
@jit
def polygons_helper(p:list[int])->bool: return len(p) != 0
#@strict
#@cache
#@inline
# TODO
#@keepit('polygons.tsv')
#@pure
#@jit
def polygons(beats:int)->list[list[int]]:
    nvs = range(3, beats+1)
    #f   = lambda nv: balanced_polygon_helper(beats, nv)
    # TODO these need to be scaled before rotation
    f   = lambda nv: rotated_polygon_helper(beats, nv)
    #f   = partial_apply(balanced_polygon_helper, beats)
    ret1 = map(f, nvs)
    #f   = lambda p: len(p) != 0
    #ret = filter(f, ret)
    ret2 = filter(polygons_helper, ret1)
    #ret = tuple(ret)

    ret3 = tuple(ret2)
    assert len(ret3) != 0

    return ret3

#@keepit('scale_polygons.tsv')
#@inline
#@pure
#@jit
def scale_polygons_impl(beats:int, b:int)->list[list[list[int]]]:
    f = lambda k: k * (beats // b)
    g = lambda p: (*p[1:], b)
    h = lambda p: tuple(map(f, g(p)))
    k = lambda n: tuple(map(h, n))
    r1 = polygons(b)
    #r = chain(r)
    r2 = map(k, r1)
    ##r = tuple(map(k, polygons(b)))
    #r = map(k, polygons(b))
    ##r = chain.from_iterable(r)
    ##r = chain(r)
    r3 = map(tuple, r2)
    r4 = tuple(r3)
    return r4
scale_polygons = mem.cache(scale_polygons_impl)
#@keepit('rotate_polygon.tsv')
#@inline
#@pure
def rotate_polygon_impl(p:list[int])->list[list[int]]:
#    #print("rotate_polygon(p=%s)" % (p,))
#    #p = map(inv_accumulate3, p)
#    p = inv_accumulate3(p)
#
#    #p = tuple(p)
#    #print("rotate_polygon p 1: %s" % (p,))
#
#    #p = map(rotations,      p)
#    p = rotations(p)
#
#    #p = tuple(p)
#    #print("rotate_polygon p 2: %s" % (p,))
#
#    #p = chain.from_iterable(p)
#    #p = tuple(p)
#    #print("rotate_polygon p 3: %s" % (p,))
#
#    p = map(accumulate,     p)
#    p = map(tuple,          p)
#    #p = accumulate(p)
#
#    p = tuple(p)
#    #print("rotate_polygon p 4: %s" % (p,))
#
#    return p
    beats = p[-1]
    g = lambda n: n - 1
    h = lambda n: n + 1
    r = set()
    # TODO
    for b in range(0, beats):
        f = lambda n: (n + b) % beats
        P = map(g, p)
        P = map(f, P)
        P = map(h, P)
        P = sorted(P)
        P = tuple(P)
        r.add(P)
    p = tuple(r)

    #print()
    #for P in p: print("rotate_polygon P: %s" % (P,))
    #print()
    #raise Exception()
    return p
rotate_polygon = mem.cache(rotate_polygon_impl)
#@keepit('rotate_polygons.tsv')
#@inline
#@pure
#@jit
def rotate_polygons_impl(nv:list[list[int]])->list[list[int]]:
    ret1 = map(rotate_polygon, nv)
    #ret = chain.from_iterable(ret)
    ret2 = tuple(ret1)
    #print("rotate_polygons ret: %s" % (ret,))
    return ret2
rotate_polygons = mem.cache(rotate_polygons_impl)

#@keepit('all_polygons.tsv')
#@inline
#@pure
def all_polygons_impl(beats:int)->list[list[int]]:
    #print("all_polygons(beats=%s)" % (beats,))
    bs = divisors(beats)
    #print("all_polygons bs 1: %s %s" % (len(bs), bs,))
    f  = lambda n: beats // n
    bs = map(f, bs)

    #bs = tuple(bs)
    #print("all_polygons bs 2: %s %s" % (len(bs), bs,))

    f  = lambda b: b >= 3
    bs = filter(f, bs)

    #bs = tuple(bs)
    #print("all_polygons bs 3: %s %s" % (len(bs), bs,))

    f = lambda b: scale_polygons(beats, b)
    bs = map(f, bs)

    #bs = tuple(bs)
    #print("all_polygons bs 4: %s %s" % (len(bs), bs,))

    # merge layers
    # TODO inelegant
    d = {}
    for c in bs:
        for b in c:     # layer
            for a in b:
                if len(a) in d: d[len(a)].append(a)
                else:           d[len(a)] = [a]

    #print()
    #print("d: %s" % (d,))
    #print()
    if beats % 2 == 0: d[2] = [(beats//2,beats,)]

    #bs = d.values()
    bs = sorted(d.items())
    bs = tuple(zip(*bs))
    bs = bs[-1]
    #bs = tuple(map(tuple, bs))
    #bs = map(tuple, bs)
    #print()
    #for c in bs:
    #    #for b in c:
    #    print("all_polygons c: %s %s" % (len(c), c,))
    #print()
    #print("all_polygons bs 5: %s %s" % (len(bs), bs,))

    bs = map(rotate_polygons, bs)
    bs = map(chain.from_iterable, bs)
    bs = map(tuple, bs)
    bs = tuple(bs)
    #print("all_polygons bs 5: %s %s" % (len(bs), bs,))

    #bs = map(set,   bs)
    #bs = map(tuple, bs)
    #bs = tuple(bs)
    #print("all_polygons bs 6: %s" % (bs,))
    return bs
all_polygons = mem.cache(all_polygons_impl)

#@keepit('all_layers.tsv')
#@inline
#@pure
#@jit
def all_layers_impl(beats:int)->list[list[list[list[int]]]]:
    #print("all_layers(beats=%s)" % (beats,))
    layers = all_polygons(beats)
    #print("all_layers layers 1: %s %s" % (len(layers), layers,))
    #for layer in layers: print("all_layers layer: %s" % (layer,))
    rs     = range(1,len(layers)+1)
    f      = lambda r: combinations(layers, r)
    #f      = lambda r: product(*layers)
    #f      = lambda r: product(layers, r)
    ret1 = map(f, rs)
    #ret = map(chain.from_iterable, ret)
    ret2 = map(tuple, ret1)

    #print()
    ret3 = chain.from_iterable(ret2)
    ret4 = tuple(ret3)
    #print("all_layers ret 2: %s %s" % (len(ret), ret,))
    #print()
    #for f in ret: print("all_layers ret 3: %s %s" % (len(f), f,))
    #print()
    #raise Exception()
    return ret4
all_layers = mem.cache(all_layers_impl)

#@keepit('expand_layers.tsv')
#@inline
#@pure
@jit
def expand_layers_impl(layers:list[list[list[list[int]]]])->list[list[list[list[list[int]]]]]:
    #print("expand_layers(layers=%s)" % (layers,))
    f  = lambda l: product(*l)
    ls1 = map(f, layers)
    ls2 = map(tuple, ls1)
    ls3 = tuple(ls2)
    #print("expand_layers ret 1: %s %s" % (len(ls),ls,))
    #print()
    #for l in ls: print("expand_layers ret 2: %s %s" % (len(l),l,))
    #print()
    return ls3
expand_layers = mem.cache(expand_layers_impl)
#@keepit('expand_layer2.tsv')
#@inline
#@pure
#@jit
def expand_layer2_impl(layer:list[list[list[list[int]]]])->list[list[list[list[list[int]]]]]:
    #print("expand_layer2(layer=%s)" % (layer,))
    f     = lambda b, l: product((b,), l)
    layer1 = starmap(f,     layer)
    layer2 =     map(tuple, layer1)
    layer3 = tuple(layer2)
    #print()
    #for l in layer: print("expand_layer2 ret 2: %s %s" % (len(l),l,))
    #print()
    return layer3
expand_layer2 = mem.cache(expand_layer2_impl)
#@keepit('expand_layers2.tsv')
#@inline
#@pure
#@jit
def expand_layers2_impl(layers:list[list[list[list[int]]]])->list[list[list[list[list[int]]]]]:
    #print("expand_layers2(layers=%s)" % (layers,))
    layers1 = map(expand_layer2, layers)
    #layers = starmap(product, layers)
    f = lambda l: product(*l)
    layers2 = map(f, layers1)
    #layers = chain(layers)
    layers3 = map(tuple, layers2)
    layers4 = tuple(layers3)
    #print()
    #for l in layers: print("expand_layers2 ret 2: %s %s" % (len(l),l,))
    #print()
    return layers4
expand_layers2 = mem.cache(expand_layers2_impl)
#@pure
#def valid_layers_helper(layers:list[list[list[list[int]]]])->list[list[list[list[int]]]]:
#    # TODO all valid combos of positive [[negative] positive]*
#    #
#    raise Exception()
#@inline
#@pure
@jit
def removeDuplicates(lst:list)->list: return tuple(set((i for i in lst)))
#@keepit('multiple_subset_sum.tsv')
#@inline
#@pure
#@jit
def multiple_subset_sum_impl(n:int, A:list[int])->list[list[int]]:
    #print("multiple_subset_sum(n=%s, A=%s)" % (n, A,))
    k1 = range(1, len(A)+1)
    f = lambda i: combinations(A, i)
    k2 = map(f, k1)
    k3 = chain.from_iterable(k2)
    #k = map(tuple, k)

    #k = tuple(k)
    #print("multiple_subset_sum k 1: %s" % (k,))
    
    #f = lambda i: map(h, i)
    g = lambda s: sum(s) == n
    k4 = filter(g, k3)
    k5 = set(k4)
    #k = removeDuplicates(k)
    k6 = tuple(k5)
    #print("multiple_subset_sum k 2: %s" % (k,))
    return k6
multiple_subset_sum = mem.cache(multiple_subset_sum_impl)
#@keepit('bit_strings.tsv')
#@inline
#@pure
def bit_strings_impl(nlayer:int)->list[list[list[list[int]]]]:
    #print("bit_strings(nlayer=%s)" % (nlayer,))
    #layers = all_layers(beats)
    s1     = (1,) * (nlayer // 1) # '1'
    s10    = (2,) * (nlayer // 2) # '10'
    s      = (*s1, *s10)
    pns    = multiple_subset_sum(nlayer, s)
    pns    = map(permutations, pns)
    pns    = chain.from_iterable(pns)
    pns    = set(pns)
    #pns = removeDuplicates(pns)

    #pns    = tuple(pns)
    #print("bitstrings pns 1: %s" % (pns,))

    d      = {
            1: (1,),
            2: (1, 0,),
    }
    g      = lambda pn: d[pn]
    f      = lambda pn: map(g, pn)
    pns    = map(f, pns)
    f      = lambda pn: chain.from_iterable(pn)
    pns    = map(f, pns)
    pns    = map(tuple, pns)
    pns    = tuple(pns)
    #print("bitstrings pns 2: %s" % (pns,))
    return pns
bit_strings = mem.cache(bit_strings_impl)

#@inline
#@pure
def valid_layers0_helper(l, b): return zip(b, l)
#@lru_cache
#@inline
#@pure
def valid_layers0_helper_l(l): return partial_apply(valid_layers0_helper, l)

# TODO
#@keepit('valid_layers0.tsv') # disk space
#@inline
#@pure
def valid_layers0_impl(k):
    B, l = k
    #f = lambda b: zip(b, l)
    f = valid_layers0_helper_l(l)
    B = map(f, B)
    #B = chain.from_iterable(B)
    B = map(tuple, B)
    B = tuple(B)
    return B
valid_layers0 = mem.cache(valid_layers0_impl)

#@keepit('is_valid_layers.tsv') # disk space
#@inline
#@pure
def is_valid_layers(bs)->bool:
    #print("is_valid_layers(bs=%s)" % (bs,))
    for l1, l2 in zip(bs[:-1], bs[1:]):
    #    print("is_valid_layers l1: %s, l2: %s" % (l1, l2,))
        b1, l1 = l1
        b2, l2 = l2
        if not b1: continue
        if     b2: continue
        if not b2 and l1 in l2:
    #        print("invalid")
            return False
    return True
#@keepit('valid_layers.tsv')
#@inline
#@pure
def valid_layers_impl(beats:int)->list[list[list[list[int]]]]:
    #print("valid_layers(beats=%s)" % (beats,))
    layers = all_layers(beats)

    #print("valid_layers layers: %s" % (layers,))

    nlayers = map(len, layers)

#    nlayers = tuple(nlayers)
    #print("valid_layers nlayers: %s" % (nlayers,))


    bs      = map(bit_strings, nlayers)

#    bs = tuple(bs)
    #print("valid_layers bs 1: %s" % (bs,))
    #raise Exception()

    #f      = lambda bs: zip(bs, layers)
    #bs = map(f, bs)
    bs = zip(bs, layers)
    
#    bs = tuple(bs)
    #print("valid_layers bs 2: %s" % (bs,))

    bs = map(valid_layers0, bs)

    bs = map(tuple, bs)
#    bs = tuple(bs)
    #print("valid_layers bs 3: %s" % (bs,))

    #bs = map(tuple, bs)
    #bs = tuple(bs)
    #print("valid_layers bs 4: %s" % (bs,))

    #print()
    #for k in bs:
    #    print("k: %s" % (k,))
    #print()

    #bs = expand_layers2(bs)
    bs = map(expand_layers2, bs)
    bs = chain.from_iterable(bs)
    bs = chain.from_iterable(bs)
    bs = map(tuple, bs)
#    bs = tuple(bs)
    #print("valid_layers bs 4: %s" % (bs,))
    #print()
    #for L in bs:
    #    for l in L:
    #        print("valid_layers l: %s" % (l,))
    #    print()
    #print()

    #f = lambda b: filter(is_valid_layers, b)
    #bs = map(f, bs)
    bs = filter(is_valid_layers, bs)

    bs = map(tuple, bs)
    bs = tuple(bs)
    #print("valid_layers bs 5: %s" % (bs,))

    #print()
    #for k in bs:
    #    print("k: %s" % (k,))
    #print()

    #bs     = starmap(is_valid_layer, bs)
    return bs
valid_layers = mem.cache(valid_layers_impl)








tetrachords = (
    (1, 1, 1,), #  0
    (1, 1, 2,), #  1
    (1, 2, 1,), #  2
    (2, 1, 1,), #  3

    (1, 2, 2,), #  4
    (2, 1, 2,), #  5
    (2, 2, 1,), #  6

    (2, 2, 2,), #  7

    (1, 1, 3,), #  8
    (1, 3, 1,), #  9
    (3, 1, 1,), # 10

    (1, 2, 3,), # 11
    (2, 1, 3,), # 12
    (1, 3, 2,), # 13
    (2, 3, 1,), # 14
    (3, 1, 2,), # 15
    (3, 2, 1,), # 16

    (2, 2, 3,), # 17
    (2, 3, 2,), # 18
    (3, 2, 2,), # 19

    (2, 3, 3,), # 20
    (3, 2, 3,), # 21
    (3, 3, 2,), # 22
)
# TODO test this
#@keepit('tetrachord_transitions.tsv')
#@inline
#@pure
def tetrachord_transitions_impl(tetrachord:list[int])->list[list[int]]:
    assert len(tetrachord) == 3
    ret = []
    if tetrachord[ 0] > 1:                       ret.append(( tetrachord[0]-1, *tetrachord[1:]))
    if tetrachord[ 0] < 3:                       ret.append(( tetrachord[0]+1, *tetrachord[1:]))
    if tetrachord[-1] > 1:                       ret.append((*tetrachord[:-1],  tetrachord[-1]-1))
    if tetrachord[-1] < 3:                       ret.append((*tetrachord[:-1],  tetrachord[-1]+1))
    if tetrachord[0]  < 3 and tetrachord[1] > 1: ret.append(( tetrachord[0]+1,  tetrachord[1]-1, *tetrachord[2:]))
    if tetrachord[0]  > 1 and tetrachord[1] < 3: ret.append(( tetrachord[0]-1,  tetrachord[1]+1, *tetrachord[2:]))
    if tetrachord[-1] > 1 and tetrachord[1] < 3: ret.append((*tetrachord[:-2],  tetrachord[1]+1,  tetrachord[-1]-1))
    if tetrachord[-1] < 3 and tetrachord[1] > 1: ret.append((*tetrachord[:-2],  tetrachord[1]-1,  tetrachord[-1]+1))
    for t in ret: assert t in tetrachords
    ret = tuple(ret)
    return ret
tetrachord_transitions = mem.cache(tetrachord_transitions_impl)

#@inline
#@pure
def valid_tetrachords_helper0(t1:list[int], t2:list[int])->int:
    s1 = sum(t1)
    s2 = sum(t2)
    d = 12 - (s1 + s2)
    return d
#@inline
#@pure
def valid_tetrachords_helper(t:tuple[list[int],list[int]])->int:
    t1, t2 = t
    return valid_tetrachords_helper0(t1, t2)
#@inline
#@pure
def valid_tetrachords_helper1(d:int)->bool:
    if d < 1 or d > 3: return False
    return True

#@inline
#@pure
def valid_tetrachords_ref(ts:list[list[int]])->bool:
    t = (*ts, ts[0])
    for t1, t2 in zip(t[:-1], t[1:]):
        s1 = sum(t1)
        s2 = sum(t2)
        d = 12 - (s1 + s2)
        if d < 1 or d > 3: return False
    return True

#@keepit('valid_tetrachords.tsv')
#@inline
#@pure
def valid_tetrachords(ts:list[list[int]])->bool:
    # half steps should not be neighbors
    # whole steps and m3 steps should not be neighbors
    # m3 steps should not be neighbors
    #print("valid_tetrachords(tetrachords=%s)" % (ts,))
    k = len(ts)
    t = (*ts, ts[0])
    t = zip(t[:-1], t[1:])
    t = map   (valid_tetrachords_helper, t)
    t = takewhile(valid_tetrachords_helper1, t)
    t = tuple(t)
    p = len(t)
    t = k == p
    if t: print("valid_tetrachords ret: %s" % (ts,), file=outfile, flush=True)
    assert t == valid_tetrachords_ref(ts)
    return t
    #for t1, t2 in zip(t[:-1], t[1:]):
    #    s1 = sum(t1)
    #    s2 = sum(t2)
    #    d = 12 - (s1 + s2)
    ##for d in t:
    #    #print("valid_tetrachords t1: %s %s" % (t1, s1,))
    #    #print("valid_tetrachords t2: %s %s" % (t2, s2,))
    #    #print("valid_tetrachords d:  %s" % (d,))
    #    if d < 1 or d > 3: return False
    ##print("True")
    #print("valid_tetrachords ret: %s" % (ts,), file=outfile, flush=True)
    #return True
#@keepit('all_tetrachords_helper.tsv')
#@inline
#@pure
def all_tetrachords_helper_impl(r:int)->list[list[int]]:
    print("all_tetrachords_helper(r=%s)" % (r,))
    #f = lambda r: combinations_with_replacement(tetrachords, r)
    #R = map(f, R)
    #R = chain.from_iterable(R)
    R = combinations_with_replacement(tetrachords, r)
    print("all_tetrachords_helper 1")
    R = set(R)

    #R = tuple(R)
    #print("all_tetrachords R 2: %s" % (R,), flush=True)
    print("all_tetrachords_helper 2")

    #f = lambda r: permutations(r)
    #R = map(f, R)
    R = map(permutations, R)
    R = map(set, R)
    R = chain.from_iterable(R)
    #R = set(R)

    #R = tuple(R)
    #print("all_tetrachords R 3: %s" % (R,))
    print("all_tetrachords_helper 3")

    #f = lambda t: valid_tetrachords(t)
    #R = filter(f, R)
    R = filter(valid_tetrachords, R)
    print("all_tetrachords_helper 4")
    #R = set(R)
    R = tuple(R)
#
    #print("all_tetrachords_helper R 4: %s" % (R,))
    print("all_tetrachords_helper R 5")
    return R
all_tetrachords_helper = mem.cache(all_tetrachords_helper_impl)
#@keepit('all_valid_tetrachords_helper.tsv')
##@inline
#@pure
#def all_valid_tetrachords_helper(r:int)->list[list[int]]:
#    R = all_tetrachords_helper(r)
#    f = lambda t: valid_tetrachords(t)
#    R = filter(f, R)
#    R = tuple(R)
#
#    print("all_tetrachords R 4: %s" % (R,))
#    return R
#@keepit('all_tetrachords.tsv')
#@inline
#@pure
def all_tetrachords()->list[list[int]]:
    print("all_tetrachords()")
    #R = range(1, len(tetrachords)+1)
    R = range(1, 7+1)
    #R = range(1, 5+1)

    #f = lambda r: all_valid_tetrachords_helper(r)
    #f = lambda r: all_tetrachords_helper(r)
    #R = map(f, R)
    R = map(all_tetrachords_helper, R)
    print("all_tetrachords R 1")

#    #R = tuple(R)
#    #print("all_tetrachords R 1: %s" % (R,), flush=True)
#
#    f = lambda r: combinations_with_replacement(tetrachords, r)
#    R = map(f, R)
    R = chain.from_iterable(R)
    print("all_tetrachords R 2")
#
#    #R = tuple(R)
#    #print("all_tetrachords R 2: %s" % (R,), flush=True)
#    print("all_tetrachords 2")
#
#    f = lambda r: permutations(r)
#    R = map(f, R)
#    R = chain.from_iterable(R)
#
#    #R = tuple(R)
#    #print("all_tetrachords R 3: %s" % (R,))
#    print("all_tetrachords 3")
#
#    f = lambda t: valid_tetrachords(t)
#    R = filter(f, R)
    R = tuple(R)
    #print("all_tetrachords R 4: %s" % (R,))
    print("all_tetrachords R 4")
    return R
#@keepit('get_scale.tsv')
#@inline
#@pure
def get_scale_impl(tetrachords:list[list[int]])->list[int]:
    print("get_scale(tetrachords=%s)" % (tetrachords,))
    ret = []
    i = 0
    j = 1
    k = 0
    while True:
        i %= len(tetrachords)
        j %= len(tetrachords)
        a = tetrachords[i]
        b = tetrachords[j]
        A = sum(a)
        B = sum(b)
        c = 12 - (A + B)
        #print("a: %s" % (a,))
        #print("b: %s" % (b,))
        #print("c: %s" % (c,))
        #print()
        assert 1 <= c
        assert c <= 3
        #ret.append((*a, c, *b))
        ret.extend((*a, c,))
        #k = (A + B + c) % 12
        k = (k + A + c) % 12
        print("get_scale k: %s, i: %s, j: %s, a: %s, c: %s, b: %s" % (k, i, j, a, c, b,))
        i += 1
        j += 1
        if k == 0 and i == len(tetrachords):
            assert j == 1
            break
        # TODO
        #raise Exception()
    ret = tuple(ret)
    print("get_scale ret: %s" % (ret,))
    assert sum(ret) % 12 == 0
    return ret
get_scale = mem.cache(get_scale_impl)
#@keepit('all_scales.tsv')
#@inline
#@pure
def all_scales()->list[list[int]]:
    print("all_scales()")
    ts = all_tetrachords()
    print("all_scales 1")
    ts = map(get_scale, ts)
    print("all_scales 2")
    ts = map(rotations, ts)
    print("all_scales 3")
    ts = chain.from_iterable(ts)
    print("all_scales 4")
    ts = set(ts)
    print("all_scales 5")
    ts = tuple(ts)
    print("all_scales ts: %s" % (ts,))
    return ts
# TODO decompose scale into component tetrachords
#def get_tetrachords(scale:list[list[int]])->list[list[int]]:
# TODO get chord combos tonic/enharmonic to scales
#def get_chords():


























# TODO to switch beats/layers, find polygons which contain a congruent subset of points ? => 8v in 8s in 16v in 16s; not less than 1v/1s apart ?

#@strict
#@inline
def polygon_layers(beats:int)->list[list[int]]:
    ret = polygons(beats)
    f   = lambda ps: choice(ps)
    ret = map(f, ret)
    #ret = chain(*ret)
    ret = tuple(ret)
    #ret = polygon_helper1(ret)
    assert len(ret) != 0
    #print("polygon_layers ret: %s" % (ret,))
    print("polygon_layers ret: %s" % (ret,))
    return ret
#@strict
#@inline # TODO inline tail?
def polygon_beats_layers(beats_min:int, beats_max:int)->list[list[int]]:
    f   = lambda beats: (beats, polygon_layers(beats))
    ret = range(beats_min, beats_max+1)
    ret = map(f, ret)
    f   = lambda pls: len(pls[-1]) != 0
    ret = filter(f, ret)
    ret = tuple(ret)
    assert len(ret) != 0
    print("polygon_beats_layers ret: %s" % (ret,))
    return ret
#@strict
#@inline
def polygon_beats_layer(beats_min:int, beats_max:int)->list[list[int]]:
    ret = polygon_beats_layers(beats_min, beats_max)
    assert len(ret) != 0
    ret = choice(ret)
    # TODO rotate each layer
    print("polygon_beats_layer ret: %s" % (ret,))
    return ret


#print(balanced(5, [0, 1, 2, 3, 4]))
#exit()
#print(valid_layers(6))
#exit()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

size = comm.Get_size()
print("Hello World from rank %s of %s" %(rank,size))

if rank == 0 and __name__ == '__main__':
    # select ratios
    # select brainwave range/frequency
    # select polygons/layers, bjorklund
    # select scale/tetrachords
    # select chord progression
    # select trichords
    
    B = base_frequency()    # resonant frequency of target molecule
    print("base frequency: %s" % (B,))
    L = limit()             # prime limit
    print("limit: %s" % (L,))
    s = scale(L)            # ratios
    print("scale: %s" % (s,))
    T = timeofday()         # time of day when song is to be played
    print("time: %s" % (T,))
    R = brainrange(T).value # brainwave range
    print("brain range: %s" % (R,))
    f = brainwave(B, s, R)  # brainwave frequency
    print("brain frequency: %s" % (f,))
    t = songtype()          # song type
    print("song type: %s" % (t,))
    nmin,nmax = beats(B, s, f, t)   # beats
    
    # generate smooth numbers
    # take all permutations with replacement s.t. pairwise the coefficients are different (don't just vary exponents)
    # given a layer, select another layer s.t. when a window is passed over the vertices each polygon is balanced
    # number of repetitions of each number should fall within the range specified by song type ? or for verse/phrase/measure length?
   
    #nmin = 16
    nmin = 8
    #nmax = 30
    nmax = 10
    n  = range(nmin, nmax+1)
    layers = map(valid_layers, n)
    layers = chain.from_iterable(layers)
    layers = tuple(layers)
    layers = choice(layers)
    l = len(layers)
    
    print("test")
    
    # TODO all combos of tetrachords s.t. 1<= 12-sum <= 3
    s = all_scales()
    s = choice(s)
    print("s: %s" % (s,))

    # TODO * chords
    # TODO - trichords
    # TODO * melodies
    # TODO * chord changes
    # TODO * scale changes
    
    
    # TODO double layers until at the desired number of instrumental voices
    
    # instrumental ranges        => rhythms
    # - infrasound (<= 20hz) => AM/FM
    # - deep bass  (20 - ~110hz) => drones, ostinatos
    # - very high  (~1k-20khz)
    # - ultrasound (>= 20khz)    => drones, ostinatos
    # vocal ranges (~100 - ~1khz) => melodies
    # - bass     1&2
    #   Bass: the lowest male voice, E2 (two Es below middle C) to E4 (the E above middle C).
    # - baritone 1&2
    #   Baritone: a male voice, G2 (two Gs below middle C) to F4 (F above middle C).
    # - tenor    1&2
    #   Tenor: the highest male voice, B2 (2nd B below middle C) to A4 (A above middle C), and possibly higher.
    # - alto     1&2
    #   Contralto: the lowest female voice, F3 (F below middle C) to E5 (2nd E above Middle C). Rare contraltos possess a range similar to the tenor.
    # - soprano  1&2
    #   Mezzo-soprano: a female voice between A3 (A below middle C) and A5 (2nd A above middle C).
    #   Soprano: the highest female voice, being able to sing C4 (middle C) to C6 (high C), and possibly higher.
    
    #n,p = polygon_beats_layer(nmin,nmax)
    #print("polygons: %s" % (p,))
    #print("beats: %s" % (n,))
    #m = relative_prime(n, int(log(n)))   # pulses
    #print("#accents: %s" % (m,))
    #b = bjorklund(n, m)     # accents
    #print("accents: %s" % (b,))
    #r = randrange(m)        # rotation
    #print("rotation: %s" % (r,))
    #b = (*b[r:], *b[:r])
    #print("accents: %s" % (b,))
    #l = randrange(13) + 1   # layers
    #print("layers: %s" % (l,))
    #p = polygon_layers(n, l)      # rhythms
    #p = polygon_layers(n)
    #l = randrange(len(p))+1
    print("layers: %s" % (l,))
    #H = Hharmony(l)         # horizontal harmony(s); keys/modes
    #v = vharmony(H)         # vertical harmony;      chords
    #h = hharmony(v)         # horizontal harmony(s); trichords/modes/styling
    #F = feet(p)             # poetic feet
    #m = melody(h, F)        # melody(s)
    
    



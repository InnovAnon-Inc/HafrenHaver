# first line: 33
def polygon_helper_impl0(g:Callable[[Callable,int,int,int],list[list[int]]], beats:int, nvertex:int, offset:int)->list[list[int]]:
    #print("polygon_helper_impl0(beats=%s, nvertex=%s, offset=%s)" % (beats, nvertex, offset,), flush=True)
    f = lambda off: g(g, beats, nvertex-1, off)
    return polygon_helper_kernel(beats, nvertex, offset, f)

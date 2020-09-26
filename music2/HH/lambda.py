#! /usr/bin/env python3

import ast
import inspect
from ast_decompiler import decompile
from numba import jit

#@jit
def f2lc (f):
	source  = inspect.getsource (f)
	return src2lc (source)
#@jit
def src2lc (source):
	code    = ast.parse (source)
	
	# TODO transform from imperative to functional style
	
	code    = RewriteName ().visit (code)
	ast.fix_missing_locations (code) # TODO ?
	#code    = ast.fix_missing_locations (code)
	
	source2 = decompile (code) # TODO how to remove comments from output ?
	#assert source == source2
	return source

#@jit	
def fd2lc (fd): return src2lc (fd.read ())

class RewriteName (ast.NodeTransformer):
	def visit_Name (self, node):
		# TODO rename to greek letters, etc
		#temp = ast.Subscript (
		#	value=ast.Name (id='data', ctx=ast.Load ()),
		#	slice=ast.Index (value=ast.Str (s=node.id)),
		#	ctx=node.ctx)
		#return ast.copy_location (temp, node)
		return node

if __name__ == "__main__":
	import os
	
	def main ():
		fname = os.path.realpath (__file__)
		with open (fname, "r") as fd: src = fd2lc (fd)
		print (src)
		for f in (f2lc, src2lc, fd2lc): print (f2lc (f))
	main ()

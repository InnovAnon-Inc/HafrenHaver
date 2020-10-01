#! /usr/bin/env python3

import ast
import astor
import inspect
#from ast_decompiler import decompile
#from numba import jit

import re

indent_amount   = 3
comment_pattern = re.compile (' *#.*')
lambda_pattern  = re.compile ('lambda *')
indent_pattern  = re.compile (' ' * indent_amount)
empty_line      = re.compile (r'^\s*$')
assert_pattern  = re.compile ('assert.*') # TODO this is dirty
print_pattern   = re.compile ('print.*')  # TODO this is dirty
# TODO replace pi, phi

def lc2str (lc):                                                        # convert code into useless text
	lc = re.sub (comment_pattern,     '',  lc)                          # strip comments
	lc = re.sub ( assert_pattern,     '',  lc)
	lc = re.sub (  print_pattern,     '',  lc)  
	lc = lc.splitlines ()                                               # remove empty lines
	f  = lambda x: not re.match (empty_line, x)
	lc = filter (f, lc)
	lc = '\n'.join (lc)
	lc = re.sub ( lambda_pattern, '\\\\', lc)                           # replace 'lambda' with greek letter
	lc = re.sub ( indent_pattern,   '\t', lc)                           # replace '   ' with '\t'
	# TODO don't delete spaces after 'if', etc.
	# TODO don't delete space around 'is'
	# ... it would be better to hack the decompiler for this
	#lc = lc.replace ( ' ',  '')                                         # delete spaces
	lc = lc.replace ('\t', ' ')                                         # TODO replace '\t' with something bizarre 
	lc = lc.replace ('\n', ' ')                                         # TODO replace '\n' with something bizarre
	return lc

##@jit
def f2lc (f):                                                           # function pointer to lambda calculus-like source
	source  = inspect.getsource (f)
	return src2lc (source)

##@jit
def src2lc (source):                                                    # source to lambda calculus-like source
	code    = ast.parse (source)

	# TODO add type info to the code, so we can strip it here
	# TODO strip annotations ?
	xforms = (RemoveImports, RemoveAssertions, RemovePrintStatements, EliminateDeadCode, ImperativeToFunctional, RewriteNames)
	for xform in xforms: code = xform ().visit (code)
	# TODO ?
	code    = ast.fix_missing_locations (code)
	#ast.fix_missing_locations (code)
	
	#source2 = decompile (code) # TODO how to remove comments from output ?
	#code = astor.strip_tree (code
	astor.to_source (code, indent_with=' ' * indent_amount)             # code.toast Dafydd is still in the closet
	#assert source == source2
	return source

##@jit	
def fd2lc (fd): return src2lc (fd.read ())                              # file descriptor to lambda calculus-like source

class RewriteNames (ast.NodeTransformer):                               # replace descriptive identifiers with explitives
	# TODO create index of all names in source
	# TODO create random mapping from old names to new names... don't use lambda!
	# TODO renaming is then a simple lookup and doesn't need to worry about context
	def visit_Name (self, node):
		# TODO rename to greek letters, etc
		#temp = ast.Subscript (
		#	value=ast.Name (id='data', ctx=ast.Load ()),
		#	slice=ast.Index (value=ast.Str (s=node.id)),
		#	ctx=node.ctx)
		#return ast.copy_location (temp, node)
		return node
		
class RemoveAssertions       (ast.NodeTransformer):                     # nix the QA
	def visit_Assert     (self, node): return None
class RemoveImports          (ast.NodeTransformer):                     # support local businesses
	def visit_Import     (self, node): return None
	def visit_ImportFrom (self, node): return None
	
class RemovePrintStatements  (ast.NodeTransformer):                     # TODO... actual hard work
	def visit_Call       (self, node): return node
class EliminateDeadCode      (ast.NodeTransformer):                     # TODO... actual hard work
	pass
class ImperativeToFunctional (ast.NodeTransformer):                     # TODO... actual hard work
	def visit_For        (self, node): return node
	def visit_AsyncFor   (self, node): return node
	def visit_While      (self, node): return node
	def visit_If         (self, node): return node

if __name__ == "__main__":
	import os
	
	def main ():
		fname = os.path.realpath (__file__)
		with open (fname, "r") as fd: src = fd2lc (fd)
		print (src)
		for f in (f2lc, src2lc, fd2lc): print (f2lc (f))
	main ()

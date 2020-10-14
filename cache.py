#! /usr/bin/env python3

from pathlib import Path

def helper (make_key, indb, getdb, setdb, f, *args):                    # this is the real logic. it seemed nice here
	#print ("helper (%s, %s, %s, %s, %s, %s)" % (make_key, indb, getdb, setdb, f, args))
	key = make_key (f, *args)
	if indb (key): return getdb (key)
	val = f (*args)
	setdb (key, val)
	return val
def indb  (key, db): return key in db
def getdb (key, db): return db[key]
def setdb (key, db, val):   db[key] = val

memoize_db = {}                                                         # but I started having second thoughts here
def memoize_key   (f, *args): return (f.__name__, *args)                # where I cache expensive operations in memory
def memoize_indb  (key):      return indb  (key, memoize_db)
def memoize_getdb (key):      return getdb (key, memoize_db)
def memoize_setdb (key, val):        setdb (key, memoize_db, val)
def memoize       (f, *args): return helper (memoize_key, memoize_indb, memoize_getdb, memoize_setdb, f, *args)

def cacher_key (f, *args): return "%s-%s.cache" % (f.__name__, str (args)) # dreadful sorry to the poor sap who reads this
def cacher_indb (key):                                                  # I thought it was basically the same thing as caching net ops on disk
	my_file = Path (key)
	return my_file.is_file ()
from ast import literal_eval as make_tuple
def cacher_getdb (key):                                                 # and getting keys is basically the same as getting cached results
	ret = key_getdb (key)
	ret = make_tuple (ret)
	return ret
def cacher_setdb (key, val):
	val = str (val)
	with open (key, "w") as f: f.write (val)
def cacher (f, *args): return helper (cacher_key, cacher_indb, cacher_getdb, cacher_setdb, f, *args)
def memoized_cacher (f, *args): return memoize (cacher, f, *args)

def nullify_helper (val, nullify):
	val2 = []
	for n in range (0, len (val)):
		if n in nullify: val2.append (None)
		else:            val2.append (val[n])
	val = tuple (val2)
	return val
def cacher_setdb2 (key, val, nullify):                                  # nullify ephemeral data which should not be cached
	val = nullify_helper (val, nullify)
	#for n in nullify: val[n] = None
	cacher_setdb (key, val)
def cacher2 (nullify, f, *args):
	sdb = lambda key, val: cacher_setdb2 (key, val, nullify)
	return helper (cacher_key, cacher_indb, cacher_getdb, sdb, f, *args)
def setdb2 (key, db, val, nullify):
	val = nullify_helper (val, nullify)
	setdb (key, db, val)
def memoize_setdb2 (key, val, nullify):        setdb2 (key, memoize_db, val, nullify)
def memoize2       (nullify, f, *args):
	sdb = lambda key, val: memoize_setdb2 (key, val, nullify)
	return helper (memoize_key, memoize_indb, memoize_getdb, sdb, f, *args)
def memoized_cacher2 (nullify, f, *args):
	g = lambda f, *a: cacher2 (nullify, f, *a)
	return memoize2 (nullify, g, f, *args)

def key_indb (key):  return cacher_indb  (key)                          # abandon all hope, ye who enter here
def key_getdb (key):
	with open (key, "r") as f: ret = f.read ()
	return ret
def key_setdb (key, val): pass	                                        # NOOP: don't overwrite the user's API keys
def key (f):
	k = lambda F, a:   "%s.key" % (f.__name__,)
	K = lambda key: None
	#return helper (k, key_indb, key_getdb, key_setdb, K, ())
	return helper (k, key_indb, key_getdb, key_setdb, K, None)
def memoized_key (f): return memoize (key, f)
		 
if __name__ == "__main__":
	def test (): return "test"
	def test2 (): pass
	def main ():
		print (         key    (test), end="")
		print (         cacher (test), end="")
		print (memoized_key    (test), end="")
		print (memoized_cacher (test), end="")
		print (memoized_key     (test2), end="")
	main ()
	quit ()

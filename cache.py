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
def memoize_key   (f, *args):
	print ("memoize_key (%s, %s)" % (f, args))
	return (f.__name__, *args)                                          # where I cache expensive operations in memory
def memoize_indb  (key):
	print ("memoize_indb (%s)" % (key,))
	return indb  (key, memoize_db)
def memoize_getdb (key):
	print ("memoize_getdb (%s)" % (key,))
	return getdb (key, memoize_db)
def memoize_setdb (key, val):
	print ("memoize_setdb (%s, %s)" % (key, val))
	setdb (key, memoize_db, val)
def memoize       (f, *args):
	print ("memoize (%s, %s)" % (f, args))
	return helper (memoize_key, memoize_indb, memoize_getdb, memoize_setdb, f, *args)

def cacher_key (f, *args):
	print ("cacher_key (%s, %s)" % (f, args))
	return "%s-%s.cache" % (f.__name__, str (args))                     # dreadful sorry to the poor sap who reads this
def cacher_indb (key):                                                  # I thought it was basically the same thing as caching net ops on disk
	print ("cacher_indb (%s)" % (key,))
	my_file = Path (key)
	return my_file.is_file ()
	
from ast import literal_eval as make_tuple

def cacher_getdb (key):                                                 # and getting keys is basically the same as getting cached results
	print ("cacher_getdb (%s)" % (key,))
	ret = key_getdb (key)
	ret = make_tuple (ret)
	return ret
def cacher_setdb (key, val):
	print ("cacher_setdb (%s, %s)" % (key, val))
	val = str (val)
	with open (key, "w") as f: f.write (val)
def cacher (f, *args):
	print ("cacher (%s, %s)" % (f, args))
	return helper (cacher_key, cacher_indb, cacher_getdb, cacher_setdb, f, *args)
def memoized_cacher (f, *args):
	print ("memoized_cacher (%s, %s)" % (f, args))
	return memoize (cacher, f, *args)



def nullify_helper (val, nullify):
	print ("nullify_helper (%s, %s)" % (val, nullify))
	val2 = []
	for n in range (0, len (val)):
		if n in nullify: val2.append (None)
		else:            val2.append (val[n])
	val = tuple (val2)
	print ("val: %s" % (val,))
	return val
def cacher_setdb2 (key, val, nullify):                                  # nullify ephemeral data which should not be cached
	print ("cacher_setdb2 (%s, %s, %s)" % (key, val, nullify))
	val = nullify_helper (val, nullify)
	#for n in nullify: val[n] = None
	cacher_setdb (key, val)
def cacher2 (nullify, f, *args):
	print ("cacher2 (%s, %s, %s)" % (nullify, f, args))
	sdb = lambda key, val: cacher_setdb2 (key, val, nullify)
	return helper (cacher_key, cacher_indb, cacher_getdb, sdb, f, *args)
def setdb2 (key, db, val, nullify):
	print ("setdb2 (%s, %s, %s, %s)" % (key, db, val, nullify))
	val = nullify_helper (val, nullify)
	setdb (key, db, val)
def memoize_setdb2 (key, val, nullify):
	print ("memoize_setdb2 (%s, %s, %s)" % (key, val, nullify))
	setdb2 (key, memoize_db, val, nullify)
def memoize2       (nullify, f, *args):
	print ("memoize2 (%s, %s, %s)" % (nullify, f, args))
	sdb = lambda key, val: memoize_setdb2 (key, val, nullify)
	return helper (memoize_key, memoize_indb, memoize_getdb, sdb, f, *args)
def memoized_cacher2 (nullify, f, *args):
	print ("memoized_cacher2 (%s, %s, %s)" % (nullify, f, args))
	g = lambda f, *a: cacher2 (nullify, f, *a)
	return memoize2 (nullify, g, f, *args)
	
def memoize_key2              (kn, f, *args):
	print ("memoize_key2 (%s, %s, %s)" % (kn, f, args))
	args = nullify_helper (args, kn)
	return memoize_key (f, *args)
def  cacher_key2              (kn, f, *args):
	print ("cacher_key2 (%s, %s, %s)" % (kn, f, args))
	args = nullify_helper (args, kn)
	return cacher_key (f, *args)
def  cacher3         (nullify, kn, f, *args):                           # nullify ephemeral key data
	print ("cacher3 (%s, %s, %s, %s)" % (nullify, kn, f, args))
	sdb = lambda key, val: cacher_setdb2 (key, val, nullify)
	ck  = lambda f, *a:    cacher_key2 (kn, f, *a)
	return helper (ck, cacher_indb, cacher_getdb, sdb, f, *args)
def memoize3         (nullify, kn, f, *args):
	print ("memoize3 (%s, %s, %s, %s)" % (nullify, kn, f, args))
	sdb = lambda key, val: memoize_setdb2 (key, val, nullify)
	mk  = lambda f, *a:    memoize_key2 (kn, f, *a)
	return helper (mk, memoize_indb, memoize_getdb, sdb, f, *args)
def memoized_cacher3 (nullify, kn, f, *args):
	print ("memoized_cacher3 (%s, %s, %s, %s)" % (nullify, kn, f, args))
	g = lambda f, *a: cacher3 (nullify, kn, f, *a)
	KN = map (lambda k: k + 1, kn) # g offsets f, which offsets args
	KN = tuple (KN)
	return memoize3 (nullify, KN, g, f, *args)
		
	

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

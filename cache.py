#! /usr/bin/env python3

from pathlib import Path

def helper (make_key, indb, getdb, setdb, f, *args):                    # this is the real logic. it seemed nice here
	key = make_key (f, *args)
	if indb (key): return getdb (key)
	val = f (*args)
	setdb (key, val)
	return val
def indb  (key, db): return key in db
def getdb (key, db): return db[key]
def setdb (key, db, val):   db[key] = val

memoize_db = {}                                                         # but I started having second thoughts here
def memoize_key   (f, *args): return (f.__name__, *args)
def memoize_indb  (key):      return indb (key, memoize_db)
def memoize_getdb (key):      return getdb (key, memoize_db)
def memoize_setdb (key, val):        setdb (key, memoize_db, val)
def memoize       (f, *args): return helper (memoize_key, memoize_indb, memoize_getdb, memoize_setdb, f, *args)

def cacher_key (f, *args): return "%s-%s.cache" % (f.__name__, str (args)) # dreadful sorry to the poor sap who reads this
def cacher_indb (key):
	my_file = Path (key)
	return my_file.is_file ()
def cacher_getdb (key):
	with open (key, "r") as f: ret = f.read ()
	return ret
def cacher_setdb (key, val):
	with open (key, "w") as f: f.write (str (val))
def cacher (f, *args): return helper (cacher_key, cacher_indb, cacher_getdb, cacher_setdb, f, *args)
def memoized_cacher (f, *args): return memoize (cacher, f, *args)

def key_indb (key):  return cacher_indb  (key)                          # abandon all hope, ye who enter here
def key_getdb (key): return cacher_getdb (key)
def key_setdb (key): pass	                                            # NOOP: don't overwrite the user's API keys
def key (f):
	k = lambda F:   "%s.key" % (f.__name__,)
	K = lambda key: None
	return helper (k, key_indb, key_getdb, key_setdb, K)
def memoized_key (f): return memoize (key, f)
		 
if __name__ == "__main__":
	def test (): return "test"
	def main ():
		print (         key    (test), end="")
		print (         cacher (test), end="")
		print (memoized_key    (test), end="")
		print (memoized_cacher (test), end="")
	main ()
	quit ()

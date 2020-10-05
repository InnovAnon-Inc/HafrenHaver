#! /usr/bin/env python3

from pathlib import Path
from ast import literal_eval as make_tuple

def cacher (f, *args):
	# TODO hash args for privacy
	fname = "%s-%s.cache" % (f.__name__, str (args))
	my_file = Path (fname)
	if my_file.is_file ():
		with open (fname, "r") as f: mylist = tuple (map (make_tuple, f))
		assert len (mylist) == 1
		mylist = mylist[0]
		#assert len (mylist) == 2
		return mylist	
	ret = f (*args)
	with open (fname, "w") as f: f.write (str (ret))
	return ret
		 
if __name__ == "__main__":
	def main ():
		# TODO
		pass
	main ()
	quit ()

#! /usr/bin/env python3

class InnovAnon (object):
	def __init__ (self, cr=None, cred=None, lic=None, *args, **kwargs):
		object.__init__ (self, *args, **kwargs)

		#if cr is None: cr = DEFAULT_COPYRIGHT
		#cr      = set (cr)
		#self.cr = cr
		
		if cred is None: cred = DEFAULT_CREDITS
		cred      = set (cred)
		self.cred = cred
		
		#if lic is None: lic = DEFAULT_LICENSE
		#lic      = set (lic)
		#self.lic = lic
		
	def extend_cr   (self, crs):   self.cr  .extend (crs) # TODO handle dups
	def extend_cred (self, creds): self.cred.extend (creds)
	def extend_lic  (self, lic):   self.lic .extend (lic)
	def copyright_str (self): return '\n'.join (self.cr)
	def   credits_str (self): return '\n'.join (self.cred)
	def   license_str (self): return '\n'.join (self.lic)
	def copyright (self): print (self.copyright_str ())
	def credits   (self): print (self.  credits_str ())
	def license   (self): print (self.  license_str ())

# TODO URL encoding
class RESTParam:
	def __init__ (self, name, value):
		assert name is not None or value is not None
		self.name  = name  # TODO URL-encode
		self.value = value # TODO URL-encode
	def __repr__ (self):
		if   self.name  is None: s = "%s"    % (self.value,)
		elif self.value is None: s = "%s="   % (self.name,)
		else:                    s = "%s=%s" % (self.name, self.value)
		return s
		
def stringify (values, j):
	if values is None: value = None
	else:
		f      = lambda v: str (v)
		values = map (f, values)
		if j is None: value = values
		else:         value = j.join (values)
	return value
	
class RESTParamList (RESTParam):
	def __init__ (self, name, values, j=',', *args, **kwargs):
		value = stringify (values, j)
		RESTParam.__init__ (self, name, value, *args, **kwargs)
class RESTParamTuple (RESTParam):
	def __init__ (self, name, values, lp='(', j=',', rp=')', *args, **kwargs):
		value = stringify (values, j)
		value = "%s%s%s" % (lp, value, rp)	
		RESTParam.__init__ (self, name, value, *args, **kwargs)
class RESTParamQuery (RESTParam):
	def __init__ (self, name, values, j='+', *args, **kwargs):
		value = stringify (values, j)
		RESTParam.__init__ (self, name, value, *args, **kwargs)

import requests

class RESTClient:
	def __init__ (self, proto, domain, api, params):
		assert proto  is not None
		self.proto  = proto
		assert domain is not None
		self.domain = domain
		self.api    = api
		#f      = lambda v: str (v)
		#params = map (f, params)
		params = stringify (params, None)
		self.params = params
	def param_str (self):
		if self.params is None: s = None
		else:                   s = '&'.join (self.params)
		return s
	def __repr__ (self):
		if self.api is None: temp = self.domain
		else:                temp = "%s/%s" % (self.domain, self.api)
		p = self.param_str ()
		if p is None: s = "%s://%s"    % (self.proto, temp)
		else:         s = "%s://%s?%s" % (self.proto, temp, p)
		return s
	def req (self, gp):
		q = str (self)
		print ("q: %s" % (q,))
		#quit ()
		r = gp (q)
		if r.status_code != 200:
			print ("error")
			return None
		r = r.json ()  # json object, various ways you can extract value
		return r
	def get  (self): return self.req (requests.get)
	def post (self): return self.req (requests.post)
		
class IARESTClient (RESTClient, InnovAnon):
	def __init__ (self, proto, domain, api, params, cr=None, cred=None, lic=None, *args, **kwargs):
		RESTClient.__init__ (self, proto, domain, api, params, *args, **kwargs)
		if cred is None:
			cred = "%s://%s" % (proto, domain)
			cred = (cred,)
		InnovAnon.__init__ (self, cr, cred, lic, *args, **kwargs)
	
if __name__ == "__main__":
	def main ():
		# TODO
		pass
	main ()
	quit ()

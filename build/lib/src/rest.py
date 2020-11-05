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
	def __init__ (self, proto, domain, api, params, session=None):
		assert proto  is not None
		self.proto  = proto
		assert domain is not None
		self.domain = domain
		self.api    = api
		#f      = lambda v: str (v)
		#params = map (f, params)
		params = stringify (params, None)
		self.params = params
		self.session = session
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
		#if r.status_code != 200:
		#	print ("error: %s" % (r,))
		#	return None
		#r = r.json ()  # json object, various ways you can extract value
		#return r
		return self.req_helper (r)
	def req_helper (self, r):
		if r.status_code != 200:
			print ("error: %s" % (r,))
			return None
		return r.json ()
	def get  (self):
		session = self.get_session ()
		return self.req (session.get)
	def post (self):
		session = self.get_session ()
		return self.req (session.post)
	def get_session (self):
		if self.session is not None: return self.session
		return requests
		
class InnovAnon2 (InnovAnon):
	def __init__ (self, proto, domain, *args, **kwargs):
		cred = "%s://%s" % (proto, domain)
		cred = (cred,)
		InnovAnon.__init__ (self, cred=cred, *args, **kwargs)
class IARESTClient (RESTClient, InnovAnon2):
	def __init__ (self, proto, domain, api, params, session=None, *args, **kwargs):
		RESTClient.__init__ (self, proto, domain, api, params, session, *args, **kwargs)
		InnovAnon2.__init__ (self, proto, domain, *args, **kwargs)
	
from constants import DEFAULT_USER_AGENT, DEFAULT_FROM
	
class HeaderRESTClient (RESTClient):
	def __init__ (self, proto, domain, api, params, session=None, send_headers=None, headers=None, *args, **kwargs):
		RESTClient.__init__ (self, proto, domain, api, params, session, *args, **kwargs)
		if send_headers is None: send_headers = {}
		if 'User-Agent' not in send_headers: send_headers['User-Agent'] = DEFAULT_USER_AGENT
		if 'From'       not in send_headers: send_headers['From']       = DEFAULT_FROM
		self.send_headers = send_headers
		self.     headers =      headers
	def req (self, gp):
		if self.send_headers is None: GP = gp
		else:                         GP = lambda q: gp (q, headers=self.send_headers)
		return RESTClient.req (self, GP)
	def req_helper (self, r):
		ret = RESTClient.req_helper (self, r)
		h = {}
		if self.headers is not None:
			for header in self.headers:
				if header not in r.headers: continue
				h[header] = r.headers[header]
			#f   = lambda h: r.headers[h]
			#h   = map (f, self.headers)
		ret = (ret, h)
		return ret
class IAHeaderRESTClient (HeaderRESTClient, InnovAnon2):
	def __init__ (self, proto, domain, api, params, session=None, send_headers=None, headers=None, *args, **kwargs):
		HeaderRESTClient.__init__ (self, proto, domain, api, params, session=session, send_headers=send_headers, headers=headers, *args, **kwargs)
		InnovAnon2.__init__ (self, proto, domain, *args, **kwargs)
		
if __name__ == "__main__":
	def main ():
		# TODO
		pass
	main ()
	quit ()

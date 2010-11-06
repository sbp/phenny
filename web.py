#!/usr/bin/env python
"""
web.py - Web Facilities
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import re, urllib
from htmlentitydefs import name2codepoint

class Grab(urllib.URLopener): 
   def __init__(self, *args): 
      self.version = 'Mozilla/5.0 (Phenny)'
      urllib.URLopener.__init__(self, *args)
   def http_error_default(self, url, fp, errcode, errmsg, headers): 
      return urllib.addinfourl(fp, [headers, errcode], "http:" + url)
urllib._urlopener = Grab()

def get(uri): 
   if not uri.startswith('http'): 
      return
   u = urllib.urlopen(uri)
   bytes = u.read()
   u.close()
   return bytes

def head(uri): 
   if not uri.startswith('http'): 
      return
   u = urllib.urlopen(uri)
   info = u.info()
   u.close()
   return info

def post(uri, query): 
   if not uri.startswith('http'): 
      return
   data = urllib.urlencode(query)
   u = urllib.urlopen(uri, data)
   bytes = u.read()
   u.close()
   return bytes

r_entity = re.compile(r'&([^;\s]+);')

def entity(match): 
   value = match.group(1).lower()
   if value.startswith('#x'): 
      return unichr(int(value[2:], 16))
   elif value.startswith('#'): 
      return unichr(int(value[1:]))
   elif name2codepoint.has_key(value): 
      return unichr(name2codepoint[value])
   return '[' + value + ']'

def decode(html): 
   return r_entity.sub(entity, html)

if __name__=="__main__": 
   main()

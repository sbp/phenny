#!/usr/bin/env python
"""
search.py - Phenny Web Search Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web

r_string = re.compile(r'("(\\.|[^"\\])*")')
r_json = re.compile(r'^[,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]+$')
env = {'__builtins__': None, 'null': None, 'true': True, 'false': False}

def json(text): 
   """Evaluate JSON text safely (we hope)."""
   if r_json.match(r_string.sub('', text)): 
      text = r_string.sub(lambda m: 'u' + m.group(1), text)
      return eval(text.strip(' \t\r\n'), env, {})
   print text
   raise ValueError('Input must be serialised JSON.')

def search(query, n=1): 
   """Search using SearchMash, return its JSON."""
   q = web.urllib.quote(query.encode('utf-8'))
   uri = 'http://www.searchmash.com/results/' + q + '?n=' + str(n)
   bytes = web.get(uri)
   return json(bytes)

def result(query): 
   results = search(query)
   if results['results']: 
      return results['results'][0]['url']
   return None

def count(query): 
   results = search(query)
   if not results['results']: 
      return '0'
   return results['estimatedCount']

def formatnumber(n): 
   """Format a number with beautiful commas."""
   parts = list(str(n))
   for i in range((len(parts) - 3), 0, -3):
      parts.insert(i, ',')
   return ''.join(parts)

def g(phenny, input): 
   """Queries Google for the specified input."""
   query = input.group(2)
   if not query: 
      return phenny.reply('.g what?')
   uri = result(query)
   if uri: 
      phenny.reply(uri)
      if not hasattr(phenny.bot, 'last_seen_uri'):
         phenny.bot.last_seen_uri = {}
      phenny.bot.last_seen_uri[input.sender] = uri
   else: phenny.reply("No results found for '%s'." % query)
g.commands = ['g']
g.priority = 'high'
g.example = '.g swhack'

def gc(phenny, input): 
   """Returns the number of Google results for the specified input."""
   query = input.group(2)
   if not query: 
      return phenny.reply('.gc what?')
   num = count(query)
   phenny.say(query + ': ' + num)
gc.commands = ['gc']
gc.priority = 'high'
gc.example = '.gc extrapolate'

r_query = re.compile(
   r'\+?"[^"\\]*(?:\\.[^"\\]*)*"|\[[^]\\]*(?:\\.[^]\\]*)*\]|\S+'
)

def gcs(phenny, input): 
   queries = r_query.findall(input.group(2))
   if len(queries) > 6: 
      return phenny.reply('Sorry, can only compare up to six things.')

   results = []
   for i, query in enumerate(queries): 
      query = query.strip('[]')
      n = int((count(query) or '0').replace(',', ''))
      results.append((n, query))
      if i >= 2: __import__('time').sleep(0.25)
      if i >= 4: __import__('time').sleep(0.25)

   results = [(term, n) for (n, term) in reversed(sorted(results))]
   reply = ', '.join('%s (%s)' % (t, formatnumber(n)) for (t, n) in results)
   phenny.say(reply)
gcs.commands = ['gcs', 'comp']

if __name__ == '__main__': 
   print __doc__.strip()

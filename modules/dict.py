#!/usr/bin/env python
"""
dict.py - Phenny Dictionary Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, urllib
import web
from tools import deprecated

formuri = 'http://wordnet.princeton.edu/perl/webwn?s='

r_li = re.compile(r'(?ims)<li>.*?</li>')
r_tag = re.compile(r'<[^>]+>')
r_parens = re.compile(r'(?<=\()(?:[^()]+|\([^)]+\))*(?=\))')
r_word = re.compile(r'^[A-Za-z0-9\' -]+$')

@deprecated
def f_wordnet(self, origin, match, args): 
   """Gives the definition of a word using Wordnet."""
   command = 'w'
   term = match.group(2)
   term = term.encode('utf-8')

   if origin.sender != '#inamidst': 
      if not r_word.match(term): 
         msg = "Words must match the regexp %s" % r'^[A-Za-z0-9\' -]+$'
         return self.msg(origin.sender, origin.nick + ": " + msg)
      if ('--' in term) or ("''" in term) or ('  ' in term): 
        self.msg(origin.sender, origin.nick + ": That's not in WordNet.")
        return

   bytes = web.get(formuri + web.urllib.quote(term)) # @@ ugh!
   items = r_li.findall(bytes)

   nouns, verbs, adjectives = [], [], []
   for item in items: 
      item = r_tag.sub('', item)
      chunks = r_parens.findall(item)
      # self.msg(origin.sender, item)
      if len(chunks) < 2: continue

      kind, defn = chunks[0], chunks[1]
      if command != 'wordnet': 
         defn = defn.split(';')[0]
      if not defn: continue
      defn = defn[0].upper() + defn[1:]

      if kind == 'n': 
         nouns.append(defn)
      elif kind == 'v': 
         verbs.append(defn)
      elif kind == 'adj': 
         adjectives.append(defn)

   if not (nouns or verbs or adjectives): 
      self.msg(origin.sender, "I couldn't find '%s' in WordNet." % term)
      return

   while len(nouns + verbs + adjectives) > 3: 
      if len(nouns) >= len(verbs) and len(nouns) >= len(adjectives): 
         nouns.pop()
      elif len(verbs) >= len(nouns) and len(verbs) >= len(adjectives): 
         verbs.pop()
      elif len(adjectives) >= len(nouns) and len(adjectives) >= len(verbs): 
         adjectives.pop()

   if adjectives: 
      adjectives[-1] = adjectives[-1] + '.'
   elif verbs: 
      verbs[-1] = verbs[-1] + '.'
   elif nouns: 
      nouns[-1] = nouns[-1] + '.'

   for (i, defn) in enumerate(nouns): 
      self.msg(origin.sender, '%s n. %r: %s' % (term, i+1, defn))
   for (i, defn) in enumerate(verbs): 
      self.msg(origin.sender, '%s v. %r: %s' % (term, i+1, defn))
   for (i, defn) in enumerate(adjectives): 
      self.msg(origin.sender, '%s a. %r: %s' % (term, i+1, defn))
f_wordnet.commands = ['wordnet']
f_wordnet.priority = 'low'

uri = 'http://encarta.msn.com/dictionary_/%s.html'
r_info = re.compile(
   r'(?:ResultBody"><br /><br />(.*?)&nbsp;)|(?:<b>(.*?)</b>)'
)

def dict(phenny, input): 
   word = input.group(2)
   word = urllib.quote(word.encode('utf-8'))

   def trim(thing): 
      if thing.endswith('&nbsp;'): 
         thing = thing[:-6]
      return thing.strip(' :.')

   bytes = web.get(uri % word)
   results = {}
   wordkind = None
   for kind, sense in r_info.findall(bytes): 
      kind, sense = trim(kind), trim(sense)
      if kind: wordkind = kind
      elif sense: 
         results.setdefault(wordkind, []).append(sense)
   result = input.group(2).encode('utf-8') + ' - '
   for key in sorted(results.keys()): 
      if results[key]: 
         result += key + ' 1. ' + results[key][0]
         if len(results[key]) > 1: 
            result += ', 2. ' + results[key][1]
         result += '; '
   result = result.rstrip('; ')
   if result.endswith('-') and (len(result) < 30): 
      phenny.reply('Sorry, no definition found.')
   else: phenny.say(result)
dict.commands = ['dict']

if __name__ == '__main__': 
   print __doc__.strip()

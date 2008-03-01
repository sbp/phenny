#!/usr/bin/env python
# coding=utf-8
"""
translate.py - Phenny Translation Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, time
import web

r_translation = re.compile(r'<div style=padding:10px;>([^<]+)</div>')

def guess_language(phrase): 
   languages = {
      'english': 'en', 
      'french': 'fr', 
      'spanish': 'es', 
      'portuguese': 'pt', 
      'german': 'de', 
      'italian': 'it', 
      'korean': 'ko', 
      'japanese': 'ja', 
      'chinese': 'zh', 
      'dutch': 'nl', 
      'greek': 'el', 
      'russian': 'ru'
   }

   uri = 'http://www.xrce.xerox.com/cgi-bin/mltt/LanguageGuesser'
   form = {'Text': phrase}
   bytes = web.post(uri, form)
   for line in bytes.splitlines(): 
      if '<listing><font size=+1>' in line: 
         i = line.find('<listing><font size=+1>')
         lang = line[i+len('<listing><font size=+1>'):].strip()
         lang = lang.lower()
         if '_' in lang: 
            j = lang.find('_')
            lang = lang[:j]
         try: return languages[lang]
         except KeyError: 
            return lang
   return 'Moon Language'

def translate(phrase, lang, target='en'): 
   babelfish = 'http://world.altavista.com/tr'
   form = {
      'doit': 'done', 
      'intl': '1', 
      'tt': 'urltext', 
      'trtext': phrase, 
      'lp': lang + '_' + target
   }

   bytes = web.post(babelfish, form)
   m = r_translation.search(bytes)
   if m: 
      translation = m.group(1)
      translation = translation.replace('\r', ' ')
      translation = translation.replace('\n', ' ')
      while '  ' in translation:
         translation = translation.replace('  ', ' ')
      return translation
   return None

def tr(phenny, input): 
   """Translates a phrase, with an optional language hint."""
   input, output, phrase = input.groups()
   phrase = phrase.encode('utf-8')
   if (len(phrase) > 350) and (not phenny.admin(input.nick)): 
      return phenny.reply('Phrase must be under 350 characters.')

   input = input or guess_language(phrase)
   if not input: 
      return phenny.reply('Unable to guess the language, sorry.')
   input = input.encode('utf-8')
   output = (output or 'en').encode('utf-8')

   if not ((input == 'en') and (output == 'en')): 
      translation = translate(phrase, input, output)
      if translation is not None: 
         translation = translation.decode('utf-8').encode('utf-8')
         if output == 'en': 
            return phenny.reply('"%s" (%s)' % (translation, input))
         else: return phenny.reply('"%s" (%s -> %s)' % \
                                   (translation, input, output))

      error = "I think it's %s, which I can't translate."
      return phenny.reply(error % input.title())

   # Otherwise, it's English, so mangle it for fun
   for other in ['de', 'ja', 'de', 'ja', 'de', 'ja', 'de', 'ja', 'de', 'ja']: 
      phrase = translate(phrase, 'en', other)
      phrase = translate(phrase, other, 'en')
      time.sleep(0.1)

   if phrase is not None: 
      return phenny.reply(u'"%s" (en-unmangled)' % phrase)
   return phenny.reply("I think it's English already.")
   # @@ or 'Why but that be English, sire.'
tr.rule = ('$nick', ur'(?:([a-z]{2}) +)?(?:([a-z]{2}) +)?["“](.+?)["”]\? *$')
tr.example = '$nickname: "mon chien"? or $nickname: fr "mon chien"?'
tr.priority = 'low'

# @@ mangle

if __name__ == '__main__': 
   print __doc__.strip()

#!/usr/bin/env python
"""
oblique.py - Web Services Interface
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, urllib
import web

definitions = 'http://code.google.com/p/phenny-ws/wiki/ServiceDefinitions'

r_item = re.compile(r'(?i)<li>(.*?)</li>')
r_tag = re.compile(r'<[^>]+>')

def mappings(uri): 
   result = {}
   bytes = web.get(uri)
   for item in r_item.findall(bytes): 
      item = r_tag.sub('', item).strip(' \t\r\n')
      if not ' ' in item: continue

      command, template = item.split(' ', 1)
      if not template.startswith('http://'): continue
      result[command] = template
   return result

def o(phenny, input): 
   """Call a webservice."""
   text = input.group(2)
   if hasattr(phenny.config, 'services'): 
      services = phenny.config.services
   else: services = definitions

   if (not o.services) or (text == 'refresh'): 
      old = o.services
      o.services = mappings(services)
      if text == 'refresh': 
         msg = 'Okay, found %s services.' % len(o.services)
         added = set(o.services) - set(old)
         if added: 
            msg += ' Added: ' + ', '.join(sorted(added)[:5])
            if len(added) > 5: msg += ', &c.'
         return phenny.reply(msg)

   if not text: 
      return phenny.reply('Try %s for details.' % services)

   if ' ' in text: 
      command, args = text.split(' ', 1)
   else: command, args = text, ''
   command = command.lower()

   if o.services.has_key(command): 
      template = o.services[command]
      template = template.replace('${args}', urllib.quote(args.encode('utf-8')))
      template = template.replace('${nick}', urllib.quote(input.nick))
      uri = template.replace('${sender}', urllib.quote(input.sender))

      bytes = web.get(uri)
      lines = bytes.splitlines()
      if lines: 
         phenny.say(lines[0][:350])
      else: phenny.reply('Sorry, the service is broken.')
   else: phenny.reply('Sorry, no such service. See %s' % services)
o.commands = ['o']
o.example = '.o servicename arg1 arg2 arg3'
o.services = {}

if __name__ == '__main__': 
   print __doc__.strip()

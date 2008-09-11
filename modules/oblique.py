#!/usr/bin/env python
"""
oblique.py - Web Services Interface
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import urllib
import web

def mappings(uri): 
   result = {}
   bytes = web.get(uri)
   for line in bytes.splitlines(): 
      if not line.startswith('<li>'): continue
      line = line.strip()
      if not line.endswith('</li>'): continue

      command, template = line[4:-5].split(' ', 1)
      if not template.startswith('http://'): continue
      result[command] = template
   return result

def o(phenny, input): 
   """Call a webservice."""
   text = input.group(2)

   if (not o.services) or (text == 'refresh'): 
      if hasattr(phenny.config, 'services'): 
         services = phenny.config.services
      else: services = 'http://swhack.jottit.com/services'

      o.services = mappings(services)
      if text == 'refresh': 
         return phenny.reply('Okay, found %s services.' % len(o.services))

   if ' ' in text: 
      command, args = text.split(' ', 1)
   else: command, args = text, ''
   command = command.lower()
   args = urllib.quote(args)

   if o.services.has_key(command): 
      template = o.services[command]
      template = template.replace('${args}', args)
      template = template.replace('${nick}', input.nick)
      uri = template.replace('${sender}', input.sender)

      bytes = web.get(uri)
      lines = bytes.splitlines()
      if lines: 
         phenny.say(lines[0])
      else: phenny.reply('Sorry, the service is broken.')
   else: phenny.reply('Sorry, no such service. See %s' % services)
o.commands = ['o']
o.example = '.o servicename arg1 arg2 arg3'
o.services = {}

if __name__ == '__main__': 
   print __doc__.strip()

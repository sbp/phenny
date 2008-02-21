#!/usr/bin/env python
"""
info.py - Phenny Information Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def doc(phenny, input): 
   """Shows a command's documentation, and possibly an example."""
   name = input.group(1)
   name = name.lower()

   if phenny.doc.has_key(name): 
      phenny.reply(phenny.doc[name][0])
      if phenny.doc[name][1]: 
         phenny.say('e.g. ' + phenny.doc[name][1])
doc.rule = ('$nick', '(?i)help +([A-Za-z]+)(?:\?+)?$')
doc.example = '$nickname: help tell?'
doc.priority = 'low'

def commands(phenny, input): 
   # This function only works in private message
   if input.startswith('#'): return
   names = ', '.join(sorted(phenny.doc.iterkeys()))
   phenny.say('Commands I recognise: ' + names + '.')
   phenny.say(("For help, do '%s: help example?' where example is the " + 
               "name of the command you want help for.") % phenny.nick)
commands.commands = ['commands']
commands.priority = 'low'

def help(phenny, input): 
   response = (
      'Hi, I\'m a bot. Say ".commands" to me in private for a list ' + 
      'of my commands, or see http://inamidst.com/phenny/ for more ' + 
      'general details. My owner is %s.'
   ) % phenny.config.owner
   phenny.reply(response)
help.rule = ('$nick', r'(?i)help(?:[?!]+)?$')
help.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

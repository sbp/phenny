#!/usr/bin/env python
"""
admin.py - Phenny Admin Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def join(phenny, input): 
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin: 
      phenny.write(['JOIN'], input.group(2))
join.commands = ['join']
join.priority = 'low'

def part(phenny, input): 
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin: 
      phenny.write(['PART'], input.group(2))
part.commands = ['part']
part.priority = 'low'

def quit(phenny, input): 
   # Can only be done in privmsg by the owner
   if input.sender.startswith('#'): return
   if input.owner: 
      phenny.write(['QUIT'])
      __import__('os')._exit(0)
quit.commands = ['quit']
quit.priority = 'low'

def msg(phenny, input): 
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin: 
      phenny.msg(input.group(2), input.group(3))
msg.rule = (['msg'], r'(#\S+) (.*)')
msg.priority = 'low'

def me(phenny, input): 
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin: 
      msg = '\x01ACTION %s\x01' % input.group(3)
      phenny.msg(input.group(2), msg)
me.rule = (['me'], r'(#\S+) (.*)')
me.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

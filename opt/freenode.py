#!/usr/bin/env python
"""
freenode.py - Freenode Specific Stuff
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def replaced(phenny, input): 
   command = input.group(1)
   response = {
      'cp': '.cp has been replaced by .u', 
      'pc': '.pc has been replaced by .u', 
      'unicode': '.unicode has been replaced by .u'
   }[command]
   phenny.reply(response)
replaced.commands = ['cp', 'pc', 'unicode']
replaced.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

#!/usr/bin/env python
"""
__init__.py - Phenny Init Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import sys, time, threading
import bot

def run_phenny(config): 
   if hasattr(config, 'delay'): 
      delay = config.delay
   else: delay = 20

   def connect(config): 
      p = bot.Phenny(config)
      p.run(config.host)

   while True: 
      connect(config)
      if not isinstance(delay, int): break

      warning = 'Warning: Disconnected. Reconnecting in %s seconds...' % delay
      print >> sys.stderr, warning
      time.sleep(delay)

def run(config): 
   t = threading.Thread(target=run_phenny, args=(config,))
   t.start()

if __name__ == '__main__': 
   print __doc__

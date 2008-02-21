#!/usr/bin/env python
"""
reload.py - Phenny Module Reloader Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import irc

def f_reload(phenny, input): 
   """Reloads a module, for use by admins only.""" 
   if not input.admin: return

   name = match.group(2)
   module = getattr(__import__('modules.' + name), name)
   reload(module)

   if hasattr(module, '__file__'): 
      import os.path, time
      mtime = os.path.getmtime(module.__file__)
      modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))
   else: modified = 'unknown'

   self.register(vars(module))
   self.bind_commands()

   phenny.reply('%r (version: %s)' % (module, modified))
f_reload.name = 'reload'
f_reload.rule = ('$nick', ['reload'], r'(\S+)')

if __name__ == '__main__': 
   print __doc__.strip()

#!/usr/bin/env python
"""
startup.py - Phenny Startup Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import threading, time

def setup(phenny): 
   # by clsn
   phenny.data = {}
   refresh_delay = 300.0

   if hasattr(phenny.config, 'refresh_delay'):
      try: refresh_delay = float(phenny.config.refresh_delay)
      except: pass

      def close():
         print "Nobody PONGed our PING, restarting"
         phenny.handle_close()
      
      def pingloop():
         timer = threading.Timer(refresh_delay, close, ())
         phenny.data['startup.setup.timer'] = timer
         phenny.data['startup.setup.timer'].start()
         # print "PING!"
         phenny.write(('PING', phenny.config.host))
      phenny.data['startup.setup.pingloop'] = pingloop

      def pong(phenny, input):
         try:
            # print "PONG!"
            phenny.data['startup.setup.timer'].cancel()
            time.sleep(refresh_delay + 60.0)
            pingloop()
         except: pass
      pong.event = 'PONG'
      pong.thread = True
      pong.rule = r'.*'
      phenny.variables['pong'] = pong

      # Need to wrap handle_connect to start the loop.
      inner_handle_connect = phenny.handle_connect

      def outer_handle_connect():
         inner_handle_connect()
         if phenny.data.get('startup.setup.pingloop'):
            phenny.data['startup.setup.pingloop']()

      phenny.handle_connect = outer_handle_connect

def startup(phenny, input): 
   import time

   if hasattr(phenny.config, 'serverpass'): 
      phenny.write(('PASS', phenny.config.serverpass))

   if hasattr(phenny.config, 'password'): 
      phenny.msg('NickServ', 'IDENTIFY %s' % phenny.config.password)
      time.sleep(5)

   # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
   for channel in phenny.channels: 
      phenny.write(('JOIN', channel))
      time.sleep(0.5)
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

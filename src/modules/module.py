# -*- coding: utf-8 -*-
"""
module.py - PyGeoBot module construction
"""

import threading

class Module (threading.Thread):
	def __init__ (self, sender='', message='', ircSock=''):
		threading.Thread.__init__(self)
		self.message = message
		self.sender = sender
		self.ircSock = ircSock
	def run (self):
		pass
	def send (self, line):
		self.ircSock.send (line + "\r\n")
	def pm (self, recipient, content):
		self.send ("PRIVMSG " + recipient + " :"+content)
			
# -*- coding: utf-8 -*-
"""
module.py - PyGeoBot module construction
"""

import threading, re

class Module (threading.Thread):
	"""
		sender - type is IRCUser, author of message
		message - message that was sent from IRC server
		ircSock - type is socket, socket in what result must be printed
	"""
	def __init__ (self, sender='', message='', ircSock=''):
		threading.Thread.__init__(self)
		self.message = message
		self.sender = sender
		self.ircSock = ircSock
	def run (self):
		pass
	def send (self, line):
		# Remove non-space whitespace
		line = re.sub(r'([\r\n\t])', '', line)
		print line
		self.ircSock.send (line + "\r\n")
	def pm (self, recipient, content):
		self.send ("PRIVMSG " + recipient + " :"+content)
			
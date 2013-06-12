# -*- coding: utf-8 -*-
"""
module.py - PyGeoBot module construction
"""

import threading, re
import sys
sys.path.append ("../")

class Module (threading.Thread):
	"""
		sender - type is IRCUser, author of message
		message - message that was sent from IRC server
		ircSock - type is socket, socket in what result must be printed
	"""
	def __init__ (self, sender='', message='', ircSock='', data={}):
		threading.Thread.__init__(self)
		self.message = message
		self.sender = sender
		self.ircSock = ircSock
		self.data = data
		self.buffer = ""
	def run (self):
		pass
	def send (self, line):
		# Remove non-space whitespace
		line = re.sub(r'([\r\n\t])', '', line)
		#print "['SENT'] " + line
		self.ircSock.send (line + "\r\n")
	def pm (self, recipient, content):
		self.send ("PRIVMSG " + recipient + " :"+content)
	def recv (self):
		linebreak = re.compile (r'[\r\n]')
		m = linebreak.search (self.buffer)
		if m:
			# contains line breaks
			res = self.buffer[:m.start()+1]
			self.buffer = self.buffer[m.end()+1:]
			res = re.sub("[\x02\x01]", "", res)
			return res
		else:
			line = self.ircSock.recv(4048)
			if line == "":
				return -1
			self.buffer += line
			return ""
			
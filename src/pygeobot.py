"""
 PyGeoBot - python IRC bot
 Author: Geohhot
"""

import toolbox
import threading
import socket
import signal
import sys

class pygeobot(threading.Thread):

	status = 0
	"""
		Status codes:
		 0 - not connected
		 1 - connecting
		 2 - connected
	"""
	statusCodes = {
		0 : 'not connected',
		1 : 'connecting', 
		2 : 'connected'
	}

	# constructor
	def __init__(self, config='', ircServerHost = '', ircServerPort='6667', ircServerPassword='', nickname='pygeobot', realname='pygeobot', username='pygeobot', debug=False):
		threading.Thread.__init__ (self)
		self._stop = threading.Event()
		# adding keyboardInterruptHandler
		signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
		if not config:
			# config file is not defined
			if not ircServerHost:
				# not enough parameters
				toolbox.die("Non config file/ircServer is defined. Please define one of those")
			else:
				# got all information to connect, write all info to self
				self.config = {
					'ircServerHost' : ircServerHost,
					'ircServerPassword' : ircServerPassword,
					'ircServerPort' : ircServerPort,
					'username' : username,
					'realname' : realname,
					'nickname' : nickname,
					'debug' : debug
				}
		else:
			# load configuration from config file
			try: 
				self.config = toolbox.loadJSON(config)
				self.configFileName = config
			except IOError:
				toolbox.die ("Unable to read config file.\n>Make sure there is file named: '"+config+"'")

	# connect function
	"""
		Must connect on new thread, IO streams must be stored in self
	"""
	def connect (self):
		# check for config to be ok
		try:
			ircServerPort = int (self.config['ircServerPort'])
		except ValueError:
			toolbox.die ("Error in congi file ("+self.configFileName+"): ircServerPort must be type of integer")
		# check if server is ok	
		self.debugPrint("Checking for server...")
		ircServerIP = ""
		try:
			ircServerIP = socket.gethostbyname(self.config['ircServerHost'])
		except socket.error:
			toolbox.die ("Unable to connect to IRC server.\n>Make sure you spelled hostname/IP right.\n>Make sure internet is conected")
		except KeyError:
			toolbox.die ("Not enough parameters given in config file. [" + self.configFileName + "]")
		# open socket to irc Server
		self.debugPrint("Semms Ok. Connecting: "+self.config['ircServerHost'] + " [" + self.config['ircServerPort'] + "]")
		self.config['ircServerIP'] = ircServerIP
		self.status = 1
		self.start()

	# run function - will start on new thread when start() function will be called
	def run (self):
		self.ircSock = socket.socket ()
		self.ircSock.connect ((self.config['ircServerIP'], int (self.config['ircServerPort'])))
		
		self.send ("NICK "+self.config['nickname'])
		self.send ("USER "+self.config['username']+ " 0 * :" + self.config['realname'])
		self.send ("JOIN #geohhot")
		while True:
			line = self.ircSock.recv(1024)
			print line[:-1]
			args = line.split()
			if args[1] == "NOTICE":
				msg = line[line.rfind(":")+1:-1]
				self.log (msg)
			if args[1] == "MODE":
				msg = line[line.rfind(":")+1:-1]
				self.log ("MODE " +args[1] + " " + msg)
			if args[1] == "PRIVMSG":
				recipient = args[2]
				content = line[line.rfind(":")+1:-1]
				contentParams = content.split()
				if (contentParams[0] == ">hello"):
					self.pm(recipient, "Ahalo bleh")
			if args[0] == "PING":
				# send pong message
				self.send ("PONG "+line[line.rfind(":"):])

	# raw send to IRC socket
	def send (self, string):
		try:
			self.ircSock.send(string + "\n\r")
			debugPrint ("[SENT]" + string)
		except NameError:
			pass

	# send PRIVMSG
	def pm (self, recipient, content):
		msg = "PRIVMSG "+recipient+" :"+content
		print msg
		self.send (msg)

	# loging messages to terminal ( and to log file if defined)
	def log (self, string):
		print (string)

	# join function
	def join (self):
		pass

	# part function
	def part (self):
		pass

	# return status of bot (i.e. status code)
	def getStatus (self):
		return self.statusCodes[self.status]

	# return status code
	def getStatusCode (self):
		return self.status

	# returns True if 
	def isDebuging (self):
		return ('debug' in self.config and self.config['debug'])

	# prints to screen if debuging is active
	def debugPrint (self, msg):
		if self.isDebuging():
			print msg

	# will quit when KeyboardInterrupt error will be thrown
	def keyboardInterruptHandler (self, signal, frame):
		print "Interrupted! Closing connections. Quiting..."
		try:
			self.ircSock.close()
		except NameError:
			pass
		self._stop.set()
		sys.exit(0)


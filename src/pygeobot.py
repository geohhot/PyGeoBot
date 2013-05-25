# -*- coding: utf-8 -*-
"""
 PyGeoBot - python IRC bot
 Author: Geohhot
"""

import toolbox
from toolbox import termcode, irccode
import threading
import socket
import signal
import sys
sys.path.append ("./src/modules/")
import requests, re, datetime
from irc import IRCMessage, IRCUser
import url

class pygeobot(threading.Thread):

	notification_string = termcode("BLUE") + "-" + termcode("BOLD") + termcode("GREEN") + "!" + termcode("ENDC") + termcode("BLUE") + "-" + termcode("ENDC") + " "

	config = {
	    "ircServerHost": "", 
	    "ircServerPort": "",
	    "ircServerPassword" : "",
	    "nickname": "", 
	    "realname": "",
	    "username": "",
	    "debug" : False,
	    "channels" : [],
	    "log" : "",
	    'auth' : ''
	}


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
	def __init__(self, config='', ircServerHost = '', ircServerPort='6667', ircServerPassword='', nickname='pygeobot', realname='pygeobot', username='pygeobot', debug=False, channels = [], log="log.txt", auth = ""):
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
					'debug' : debug,
					'channels' : channels,
					'log' : log,
					'auth' : auth
				}
		else:
			# load configuration from config file
			try: 
				self.config = toolbox.loadJSON(config)
				self.configFileName = config
			except IOError:
				toolbox.die ("Unable to read config file.\n>Make sure there is file named: '"+config+"'")

		# open config file
		if self.config['log']:
			self.log_file = open (self.config['log'], "w")
			self.log_file.write ("Log started at %s.\n" % datetime.datetime.now().strftime("%I:%M %p on %B %d, %Y"))
			self.log_file.flush()

	# connect function
	"""
		Must connect on new thread, IO streams must be stored in self
	"""
	def connect (self):
		# check for config to be ok
		self.log (termcode("GREEN") + "================================================")
		try:
			ircServerPort = int (self.config['ircServerPort'])
		except ValueError:
			toolbox.die ("Error in congi file ("+self.configFileName+"): ircServerPort must be type of integer")
		# check if server is ok	
		self.log ("Checking for server...")
		ircServerIP = ""
		try:
			ircServerIP = socket.gethostbyname(self.config['ircServerHost'])
		except socket.error:
			toolbox.die ("Unable to connect to IRC server.\n>Make sure you spelled hostname/IP right.\n>Make sure internet is conected")
		except KeyError:
			toolbox.die ("Not enough parameters given in config file. [" + self.configFileName + "]")
		# open socket to irc Server
		self.log ("Semms Ok. Connecting: "+self.config['ircServerHost'] + " [" + self.config['ircServerPort'] + "]")
		self.log ( "================================================"  + termcode("ENDC"))
		self.config['ircServerIP'] = ircServerIP
		self.status = 1
		self.start()

	# run function - will start on new thread when start() function will be called
	def run (self):
		self.ircSock = socket.socket ()
		self.ircSock.connect ((self.config['ircServerIP'], int (self.config['ircServerPort'])))
		
		try:
			if self.config['ircServerPassword']:
				self.send ("PASS "+self.config['ircServerPassword'])
		except KeyError:
			pass
		self.send ("NICK "+self.config['nickname'])
		self.send ("USER "+self.config['username']+ " 0 * :" + self.config['realname'])
		# check if nick is taken
		while True:
			line = self.ircSock.recv(2048)
			if self.parse (line):
				break

		# send auth message
		if self.config['auth']:
			self.send (self.config['auth'])

		# join channels (wip)
		for chan in self.config["channels"]:
			self.send ("JOIN "+chan)

		while True:
			line = self.ircSock.recv(2048)
			self.parse (line)

	# parse messages from IRC server
	def parse (self, line):
		line.strip()
		line = line.decode('utf-8')
		self.debugPrint (line)
		args = line.split()
		try: 
			if int(args[1]):
				# returned status code
				if args[1] == "001":
					# welcome message, so nickname is ok
					return True
				if args[1] == "433":
					# nickname is taken, change it and resend
					self.config['nickname'] = self.config['nickname']+"_"
					self.send ("NICK "+self.config['nickname'])
					self.send ("USER "+self.config['username']+ " 0 * :" + self.config['realname'])
		except ValueError:
			pass
		if args[1] == "NOTICE":
			msg = line[line.rfind("NOTICE"):-1]
			self.log (termcode("DARK_BLUE") + msg + termcode("ENDC"))
		if args[1] == "MODE":
			msg = line[line.find("MODE"):]
			self.log (termcode("DARK_YELLOW") + msg + termcode("ENDC"))
		if args[1] == "PRIVMSG":
			# print pretty output
			msg = IRCMessage(line)
			self.log (termcode("BOLD") + termcode('GREEN') + "<"+msg.author+"> "+ termcode ('ENDC') + termcode("BLUE") + msg.recipient + termcode("YELLOW") +" : "+msg.content + termcode("ENDC"))
			contentParams = msg.content.split()
			user = IRCUser(args[0])
			# checking for URLs
			url_module = url.URLModule(sender=user, message=msg, ircSock=self.ircSock)
			url_module.start()
			# checking for commands
			if (contentParams[0] == ">hello"):
				self.pm(msg.recipient, termcode("GREEN") + " Ahalo bleh " + termcode("ENDC"))
		if args[0] == "PING":
			# send pong message
			self.send ("PONG "+line[line.rfind(":"):])
		if args[1] == "JOIN":
			# join message
			who_joined = IRCUser(args[0])
			self.log (self.notification_string +termcode("BOLD") + termcode("DARK_BLUE") + who_joined.nick + termcode("ENDC") +termcode("DARK_MAGENTA") + " [" + termcode("DARK_GREEN") + who_joined.hostname + termcode("DARK_MAGENTA") + "]" + termcode("ENDC") + " has joined " + termcode("BOLD") + args[2] + termcode("ENDC"))
		if args[1] == "PART":
			# someone left channel
			who_left = IRCUser(args[0])
			self.log (self.notification_string + termcode("STRIKE") + termcode("DARK_BLUE") + who_left.nick + termcode("ENDC") +termcode("DARK_MAGENTA") + " [" + termcode("DARK_GREEN") + who_left.hostname + termcode("DARK_MAGENTA") + "]" + termcode("ENDC") + " has left " + termcode("BOLD") + args[2] + termcode("ENDC"))

	# raw send to IRC socket
	def send (self, string):
		try:
			# Remove non-space whitespace
			string = re.sub(r'([\r\n\t])', '', string)
			self.ircSock.send(string + "\n\r")
			self.debugPrint ("[SENT]" + string)
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
		# remove all colory things from string
		#\033[%sm
		string = re.sub (r'\033\[\d*m', '', string)
		string = re.sub (r'\002\[\d*m', '', string)
		try:
			self.log_file.write (string + "\n")
			self.log_file.flush()
		except Exception:
			pass

	# join function
	def join (self, *channels):
		for chan in channels:
			# add to toJoin list
			try: 
				self.config["channels"].append (chan)
			except KeyError:
				self.config["channels"] = []
				self.config["channels"].append (chan)

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
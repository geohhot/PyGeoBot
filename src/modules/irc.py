class IRCMessage:
	def __init__ (self, privmsg_line):
		args = privmsg_line.split()
		self.recipient = args[2]
		self.author = privmsg_line[1:privmsg_line.find("!")]
		self.content = privmsg_line[privmsg_line.find(':',privmsg_line.find(self.recipient)+1)+1:]
	def get_reply_to(self):
		if self.recipient[0:1] != "#":
			# its not a channel
			return self.author
		else:
			return self.recipient

class IRCUser:
	def __init__ (self, string):
		self.nick = string[1:string.find("!")]
		self.hostname = string[string.find("!")+1:]
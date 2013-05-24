import module
from irc import IRCMessage, IRCUser
import sys
sys.path.append ("../")
import toolbox
from toolbox import irccode
import requests, re

class URLModule(module.Module):
	def run (self):
		if self.message.content:
			contentParams = self.message.content.split()
			for url in contentParams:
				if toolbox.is_proper_url (url):
					# check if url is YOUTUBE url

					try:
						# get URL's title
						resp = requests.get(url)
						# print it
						title = resp.text[resp.text.find("<title>")+7:resp.text.find("</title>")]
						# send it back
						if title:
							self.pm (self.message.get_reply_to(), irccode("DARK_MAGNETA") + "Link Title: " + irccode("PURPLE") + title)
					except Exception:
						pass
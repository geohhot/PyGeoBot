# -*- coding: utf-8 -*-
import module
import youtube, twitter # modules
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
				# check if url is YOUTUBE url
				match = toolbox.is_youtube_url (url)
				#print match
				if match:
					#ding ding: youtube URL, pass it to YT module
					new_message = self.message
					new_message.content = match.group()
					youtube_module = youtube.YouTubeModule(sender=self.sender, message=new_message, ircSock=self.ircSock)
					youtube_module.run()
					continue
				match = toolbox.is_twitter_url (url)
				if match:
					# twitter url found
					# get id, and give it to twitter module
					post_id = re.search (r'status/\d+', url).group()[7:]
					new_message = self.message
					new_message.content = post_id
					twitter_module = twitter.TwitterModule(sender=self.sender, message=new_message, ircSock=self.ircSock, data=self.data)
					twitter_module.run()
					continue
				if toolbox.is_proper_url (url):
					#print "Found url: "+url
					try:
						# get URL's title
						resp = requests.get(url)
						# print it
						title = resp.text[resp.text.find("<title>")+7:resp.text.find("</title>")]
						# send it back
						if title:
							#print title
							self.pm (self.message.get_reply_to(), irccode("DARK_MAGNETA") + "Link Title: " + irccode("PURPLE") + title)
					except Exception:
						pass

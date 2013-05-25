# -*- coding: utf-8 -*-
import module
from irc import IRCMessage, IRCUser
import sys
sys.path.append ("../")
import toolbox
from toolbox import irccode
import requests, re

class YouTubeModule(module.Module):
	YOUTUBE_REST_API = "http://gdata.youtube.com/feeds/api/videos/"
	"""
		Checks if URL is YouTube URL, if yes prints some information about it
		self.message - should contain youtube URL, so this module will parse URL
	"""
	def run (self):
		#print "YouTube module has started."
		# double check if URL is fine ?
		match = toolbox.is_youtube_url(self.message.content)
		if match:
			url = match.group()
			# now its ok, so at first get video id
			long_url_re = re.compile ("(\?|&)v=[-\w]*")
			short_url_re = re.compile ("youtu.be/[-\w]*")
			vid = ""
			ml = long_url_re.search(url)
			ms = short_url_re.search(url)
			if ml:
				vid = ml.group()[3:]
			elif ms:
				vid = ms.group()[9:]
			else:
				#print "OOps!"
				return
			# then do GET request
			#print "vid: " + vid
			data = {
				'alt' : 'json'
			}
			try:
				resp = requests.get (self.YOUTUBE_REST_API+vid, params=data)
				#print "URL: "+resp.url
				json = resp.json()
				view_count = json['entry']['yt$statistics']['viewCount']
				view_count = int (view_count)
				# make view count like 12k / 5k
				if view_count >= 1000000000:
					view_count /= 1000000000
					view_count = ("%.1f") % view_count + "b"
				elif view_count >= 1000000:
					view_count /= 1000000
					view_count = ("%.1f") % view_count + "m"
				elif view_count >= 1000:
					view_count /= 1000
					view_count = ("%.1f") % view_count + "k"
				average_rating = json['entry']['gd$rating']['average']
				average_rating = ("%.1f") % average_rating
				title = str(json['entry']['title']['$t'])
				author = str(json['entry']['author'][0]['name']['$t'])

				self.pm (self.message.get_reply_to(), irccode("CYAN") + "You" + irccode("DARK_RED") + "Tube: " + irccode("GREENISH") + title)
				self.pm (self.message.get_reply_to(), irccode("MAGNETA") + "Stats: " + irccode("GREEN") + "Views: "+view_count + irccode("GREEN") + " Rating: "+average_rating + irccode("BLUE") + " Author: "+author )
			except Exception:
				# something went wrong, could be of wrong url
				pass
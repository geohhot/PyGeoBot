# -*- coding: utf-8 -*-
import module
from irc import IRCMessage, IRCUser
import sys
sys.path.append ("../")
import toolbox
from toolbox import irccode
import requests, re

import base64 # for encoding

class TwitterModule (module.Module):
	"""Twitter module for parsing twitter links
		- client credentials must be in self.data dictionary
	"""
	TWITTER_BEARER_TOKEN = "https://api.twitter.com/oauth2/token"
	TWITTER_REST_STATUS = 'https://api.twitter.com/1.1/statuses/show.json'

	def run(self):
		# check if we have access token ?
		access_token = ""
		try:
			access_token = self.data['access_token']
		except KeyError:
			# no acces token :/ gota make one
			# step1:  get credentials
			credentials = self.data['consumer']
			credentials_encoded = base64.b64encode (credentials['key'].encode("ascii") + ":" + credentials['secret'].encode("ascii"))
			# step2: obtain a bearer token
			headers = {
				'Authorization' : 'Basic '+credentials_encoded,
				'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'
			}
			data = {
				'grant_type' : 'client_credentials'
			}
			bearer = requests.post (self.TWITTER_BEARER_TOKEN, headers=headers, data=data)
			bearer_json = bearer.json()
			# check if its ok
			if bearer.status_code == 200: #everything is ok
				access_token = bearer_json['access_token']
			else:
				access_token = "" #empty if there is an error

		# now we have access_token
		if not access_token:
			# some troubles
			pass
		else:
			try:
				# do GET request
				#print access_token
				auth = {
					'Authorization' : 'Bearer '+access_token
				}
				params = {
					'id': self.message.content
				}
				#print "ID: "+ str(self.message.content)
				tweet = requests.get (self.TWITTER_REST_STATUS, headers=auth, params=params)
				tweet = tweet.json()
				#print tweet
				reply = irccode('MAGNETA') + tweet['user']['name'] + ": " + irccode('RESET') + tweet['text']
				#print reply
				self.pm (self.message.get_reply_to(), reply)
			except Exception:
				# something went wrong hm..
				pass

# -*- coding: utf-8 -*-
"""
 toolbox - helper library for project PyGeoBot
 Autho: Geohhot
"""

import json
import sys
import re

def die (msg):
	print (msg)
	sys.exit (-1)

def loadJSON (filename):
	file = open (filename, "r")
	return json.load(file)

# taken from stack overflow
CODE = {
    'ENDC':0,  # RESET COLOR
    'BOLD':1,
    'UNDERLINE':4,
    'BLINK':5,
    'INVERT':7,
    'CONCEALD':8,
    'STRIKE':9,
    'GREY30':90,
    'GREY40':2,
    'GREY65':37,
    'GREY70':97,
    'GREY20_BG':40,
    'GREY33_BG':100,
    'GREY80_BG':47,
    'GREY93_BG':107,
    'DARK_RED':31,
    'RED':91,
    'RED_BG':41,
    'LIGHT_RED_BG':101,
    'DARK_YELLOW':33,
    'YELLOW':93,
    'YELLOW_BG':43,
    'LIGHT_YELLOW_BG':103,
    'DARK_BLUE':34,
    'BLUE':94,
    'BLUE_BG':44,
    'LIGHT_BLUE_BG':104,
    'DARK_MAGENTA':35,
    'PURPLE':95,
    'MAGENTA_BG':45,
    'LIGHT_PURPLE_BG':105,
    'DARK_CYAN':36,
    'AUQA':96,
    'CYAN_BG':46,
    'LIGHT_AUQA_BG':106,
    'DARK_GREEN':32,
    'GREEN':92,
    'GREEN_BG':42,
    'LIGHT_GREEN_BG':102,
    'BLACK':30,
}

def termcode (color):
	try:
		return '\033[%sm'%CODE[color]
	except KeyError:
		return ""

# yet not all colors are in
IRC_COLOR = {
	"WHITE" : 48,
	"BLACK" : 49,
	"RED" : 50,
	"ORANGE" : 51,
	"YELLOW" : 52,
	"LIGHT_GREEN" : 53,
	"GREEN" : 54,
	"BLUE_GREEN": 55,
	"CYAN" : 56,
	"LIGHT_BLUE" : 57,
	"BLUE" : 58,
	"PURPLE" : 59,
	"MAGNETA" : 60,
	"PURPLE_RED" : 61,
	"LIGHT_GRAY" : 62,
	"DARK_GRAY" : 63,
	
	"DARK_RED" : 68,
	"DARK_ORANGE" : 65,
	"DARK_YELLOW" : 66,
	"DARK_LIGHT_GREEN" : 67,
	"DARK_GREEN" : 68,
	"DARK_BLUE_GREEN": 69,
	"DARK_CYAN" : 70,
	"DARK_LIGHT_BLUE" : 71,
	"DARK_BLUE" : 72,
	"DARK_PURPLE" : 70,
	"DARK_MAGNETA" : 74,
	"DARK_PURPLE_RED" : 75,

	"GREENISH" : 73,
	"RESET" : 0,
	"INVERT" : 0
}

def irccode (color):
	try:
		if color == "RESET":
			return  ("%s") % ('\x03')
		elif color == "INVERT":
			return "\x10"
		else:
			result = ("%c%i") % (0x03, IRC_COLOR[color])
			return result
	except KeyError:
		return ""

# youtube regex - from stak overflow
def is_youtube_url (url):
	youtube_re = re.compile(r'(https?://)?(www\.)?youtube\.(com|nl)/watch\?v=([-\w]+)')
	youtube_short_re = re.compile("(https?://)?(www\.)?youtu\.be/[-\w]+")
	long_match = youtube_re.match (url)
	if long_match:
		return long_match
	short_match = youtube_short_re.match (url)
	if short_match:
		return short_match
	else:
		return False

# from stak overflow: "django url validation regex"
def is_proper_url (url):
	regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if regex.match (url) != None:
		return True
	else:
		return False

# checks if given URL is twitters one
def is_twitter_url (url):
	twitter_url = re.compile(
		r'(https?://)?'
		r'(www\.)?'
		r'twitter\.com/'
		r'[a-zA-Z0-9]+' # username
		r'/'
		r'status/'
		r'\d+' # status id,
		,re.IGNORECASE)
	m = twitter_url.match (url)
	if m:
		return m
	else:
		return False

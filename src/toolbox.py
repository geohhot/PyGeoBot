"""
 toolbox - helper library for project PyGeoBot
 Autho: Geohhot
"""

import json
import sys

def die (msg):
	print (msg)
	sys.exit (-1)

def loadJSON (filename):
	file = open (filename, "r")
	return json.load(file)
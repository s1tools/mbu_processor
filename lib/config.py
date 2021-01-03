#!/usr/bin/python

import ConfigParser,os

thisFile=os.path.realpath(__file__)

#print "config.py real path: ", thisFile

ini=ConfigParser.SafeConfigParser()

#Config file
#Second config file, if present, override the first one
ini.read([os.path.split(thisFile)[0]+"/config.ini","/config.ini","/config-local.ini"])
#ini.get('ocnVariable','alongTrackResolution')

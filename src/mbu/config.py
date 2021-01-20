#!/usr/bin/python

import os

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import ConfigParser as SafeConfigParser

this_file = os.path.realpath(__file__)

# print "config.py real path: ", thisFile

ini = SafeConfigParser()

# Config file
# Second config file, if present, override the first one
ini.read([os.path.split(this_file)[0] + "/config.ini", "/config.ini", "/config-local.ini"])
# ini.get('ocnVariable','alongTrackResolution')

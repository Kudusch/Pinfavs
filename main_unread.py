#!/usr/bin/python

from pinboard import *
import os
import sys
import json
import fileinput
import string
from subprocess import call

args = sys.argv[1]
args = json.loads(args)

try:
	addBookmark(args['url'], args['urlTitle'], args['description'], args['tags'], "yes")
	print(args['url'])
	call(["afplay", "return.aiff"], stdout=open(os.devnull, 'wb'))
except:
	call(["afplay", "return.aiff"], stdout=open(os.devnull, 'wb'))
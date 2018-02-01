#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import re
import os
import string
import json
import requests
from pinboard import *
from subprocess import check_output
from workflow import Workflow3

wf = Workflow3()
args = wf.args

try:
    p = re.compile(ur'(|\s)\((.*?)\)')
    description = re.search(p, args[0]).group(2)
    args = re.sub(p, '', args[0])
except:
    args = args[0]
    description = ""
args = args.split(" ")

if (wf.cached_data_fresh('tags', 600)):
    userTags = json.loads(wf.cached_data('tags', max_age=600))
else:
    wf.cached_data('tags', getTags, max_age=600)
    userTags = json.loads(wf.cached_data('tags', max_age=600))

r = re.compile(ur'^http(s|)://')
if (re.search(r, args[0])):
    url = args[0]
    tags = " ".join(args[1:])
else:
    url = check_output(['osascript', '-e', 'tell application "Safari" to return url of current tab of window 1']).rstrip()
    tags = " ".join(args)

urlTitle = getInfo()
title = 'Add: ' + urlTitle
if (tags == "" and description == ""):
    subtitle = 'Without tags or description.'
elif (not tags == "" and description == ""):
    subtitle = 'Tags: ' + tags
elif (tags == "" and not description == ""):
    subtitle = 'Description: ' + description
else:
    subtitle = 'Tags: ' + tags + ' | Description: ' + description

try:
    arg = json.dumps({'url' : url, 'urlTitle' : urlTitle, 'description' : description, 'tags' : tags})
except:
    arg = json.dumps({'url' : url, 'urlTitle' : urlTitle, 'description' : "", 'tags' : tags})

# Add an item to Alfred feedback
wf.add_item(title=title, subtitle=subtitle, arg=arg, autocomplete=None, valid=True)

try:
    for t, c in sorted(userTags.iteritems(), key=lambda item: -item[1]):
        if (args[len(args) - 1].lower() in t.lower() and not args[len(args) - 1].lower() == t.lower()):
            if (args[len(args) - 1] == ""):
                wf.add_item(title=t, subtitle=c, arg=None, autocomplete=" ".join(args) + "" + t, valid=False, uid=t)
            else:
                if (args[0] == " "):
                    wf.add_item(title=t, subtitle=c, arg=None, autocomplete=" ".join(args[:-1]) + "" + t, valid=False, uid=t)
                else:
                    wf.add_item(title=t, subtitle=c, arg=None, autocomplete=" ".join(args[:-1]) + " " + t, valid=False, uid=t)
except:
    pass
# Send feedback
wf.send_feedback()
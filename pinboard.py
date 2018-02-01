#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import requests
import sys
import json
from subprocess import check_output
from bs4 import BeautifulSoup

apiKey = os.environ['apikey']

def getInfo():
    title = check_output(['osascript', '-e', 'tell application "Safari" to return name of current tab of window 1 as text']).rstrip()
    return title.decode('utf-8')

def addBookmark(url, title, extended, tags, toread):
    global apiKey
    apiBase = "https://api.pinboard.in/v1/"
    
    arguments = {"auth_token": apiKey, "url": url, "description": title, "extended": extended, "tags": tags, "toread": toread}
    method = "posts/add"
    r = requests.get(apiBase + method, arguments)
    if (r.status_code == 200):
        return True
    else:
        return False

def getTags():
    global apiKey
    apiBase = "https://api.pinboard.in/v1/"
    arguments = {"auth_token": apiKey}
    method = "tags/get"
    r = requests.get(apiBase + method, arguments)
    soup = BeautifulSoup(r.text, "html.parser")
    tags = {}
    for t in soup.find_all('tag'):
        tags.update({t['tag'] : int(t['count'])})
        
    if (r.status_code == 200):
        return json.dumps(tags)
    else:
        return False
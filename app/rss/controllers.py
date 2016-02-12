from flask import Blueprint, make_response
import requests
from app.utils.msg_tools import ResponseTools as msg_tools
import xmltodict
import json
###########################################################################
# blueprint for flask
rss = Blueprint('rss', __name__, url_prefix='/rss')

###########################################################################
bodybuilding_feed = []
powerlifting_feed = []
crossfit_feed = []


def get_bodybuilding():
    global bodybuilding_feed
    headers = {"user-agent" : "python:com.campfirebros.exercisedb:v1..0.0"}
    r = requests.get("https://www.reddit.com/r/bodybuilding/.rss", headers=headers)
    s = xmltodict.parse(r.text)
    entries = []
    for post in s["feed"]["entry"]:
        entry = {
            'user': post['author']['name'],
            'content': post['content']['#text']
        }
        entries.append(entry)
    bodybuilding_feed = entries


def get_powerlifting():
    global powerlifting_feed
    headers = {"user-agent" : "python:com.campfirebros.exercisedb:v1..0.0"}
    r = requests.get("https://www.reddit.com/r/powerlifting/.rss", headers=headers)
    s = xmltodict.parse(r.text)
    entries = []
    for post in s["feed"]["entry"]:
        entry = {
            'user': post['author']['name'],
            'content': post['content']['#text']
        }
        entries.append(entry)
    powerlifting_feed = entries


def get_crossfit():
    global crossfit_feed
    headers = {"user-agent" : "python:com.campfirebros.exercisedb:v1..0.0"}
    r = requests.get("https://www.reddit.com/r/crossfit/.rss", headers=headers)
    s = xmltodict.parse(r.text)
    entries = []
    for post in s["feed"]["entry"]:
        entry = {
            'user': post['author']['name'],
            'content': post['content']['#text']
        }
        entries.append(entry)
    crossfit_feed = entries


@rss.route('/bodybuilding')
def bodybuilding():
    return json.dumps(bodybuilding_feed)


@rss.route('/powerlifting')
def powerlifting():
    return json.dumps(powerlifting_feed)


@rss.route('/crossfit')
def crossfit():
    return json.dumps(crossfit_feed)


get_bodybuilding()
get_crossfit()
get_powerlifting()

from flask import Blueprint, make_response
import requests
from app.utils.msg_tools import ResponseTools as msg_tools
import xmltodict
import json
###########################################################################
# blueprint for flask
rss = Blueprint('rss', __name__, url_prefix='/rss')

###########################################################################


@rss.route('/bodybuilding')
def bodybuilding():
    headers = {"user-agent" : "python:com.campfirebros.exercisedb:v1..0.0"}
    r = requests.get("https://www.reddit.com/r/bodybuilding/.rss", headers=headers)
    print r.text
    print r
    s = xmltodict.parse(r.text)
    entries = []
    html = ''
    for post in s["feed"]["entry"]:
        entry = {
            'user': post['author']['name'],
            'content': post['content']['#text']
        }
        entries.append(entry)
        html += post['content']['#text']
        html += "<br><br><br>"
        print post
    return json.dumps(entries)


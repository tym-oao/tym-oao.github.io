##This is my code.

```
#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
from flask_slack import Slack
import os

from remotes import provision_geo_data, provision_weather_data

# Mac OS certs: still hard (comment out before linux deploy)
import requests
requests.packages.urllib3.disable_warnings()


# Intantiate app
app = Flask(__name__)
api = Api(app)
slack = Slack(app)
app.add_url_rule('/slack-where', view_func=slack.dispatch)

slack_token = os.getenv('SLACKTOKEN')
slack_team = os.getenv('SLACKTEAM')


# Slash commands for Slackbot
@slack.command('where', token=slack_token,
               team_id=slack_team, methods=['POST'])
def whereami(**kwargs):
    geo = provision_geo_data()['location']
    w3w = geo['w3w_url']
    words = geo['what3words']
    lat = geo['latitude']
    lng = geo['longitude']

    slackloc = '<%s|%s>  \n%s, %s' % (w3w, words, lat, lng)
    return slack.response(slackloc)


```

---

## This is another slide

Hey, just seeing if this works

- If it does, I'll be pretty happy. <!-- .element: class="fragment" -->
- Hey this could be game-changing for me! <!-- .element: class="fragment" -->

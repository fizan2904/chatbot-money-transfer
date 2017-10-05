from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import urllib

import json, os, requests, sys, uuid, hashlib, redis

from datetime import datetime
from flask import Flask, request, make_response, render_template, send_from_directory, redirect
from flask_debugtoolbar import DebugToolbarExtension

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

from process_request import process_request

r = redis.Redis(host='localhost')

app = Flask(__name__, static_url_path='')

@app.route('/webhook', methods=["POST"])
def webhook():
	req = request.get_json(silent=True, force=True)
	if(req.get('result').get('action') == "confirm_transfer"):
		return render_template('mpin.html')
	res = process_request(req)
	res = json.dumps(res, indent=4)
	r = make_response(res)  
	r.headers['Content-Type'] = 'application/json'
	return r

@app.route('/authorize')
def auth():
	req = request
	url = req.url
	parsed = urllib.parse.parse_qs(url)
	print(parsed)
	auth_token = parsed['http://12413345.ngrok.io/authorize?account_linking_token'][0]
	redirect_url = parsed['redirect_uri'][0]
	return render_template('auth.html', redirect_url=redirect_url)
	#process_auth(req, auth_token, redirect_url)

@app.route('/login', methods=["POST"])
def login():
	username = request.form.get('username')
	password = request.form.get('password')
	redirect_url = request.form.get('redirect_url')+ '&authorization_code='+ username
	if(password == "fizan"):
		print("---------------")
		print(redirect_url)
		r = requests.get(redirect_url)
		if(r.status_code == 200):
			return render_template('success.html')
	else:
		return "Request did not contain redirect_uri and username in the query string"
	
if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)
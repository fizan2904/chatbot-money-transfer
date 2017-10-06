import requests, redis
import json
from flask import render_template

r = redis.Redis(host='localhost')

def fb_login_template(user_id):
	data = {
        "recipient": {"id": user_id},
        "message": {"attachment": {
        		"type":"template",
        		"payload":{
					"template_type":"button",
					"text":"Please login",
					"buttons":[{
						"type": "account_link",
						"url": "https://9a2a2130.ngrok.io/authorize",
						"webview_height_ratio": "compact"
					}]
				}
        	}
        }
    }
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAAb3lzmGmJcBAPTUWrJtcsGTzoHhVHzWpwUbXTHFLZBKJ79XDKZCLflSEkesDeNEcQOOF71Ru1dhvvignYf7Pza7SYxKIhCmMxOF84QrTZAa8igyNp3zCXM3ZC0O8CLS5kx73DZBgZAO4hjrF4ZB96qYWDN6EeUd4QGUGxaHxmdFgZDZD", json=data)
	print(resp.content)

def fb_yes_no_template(user_id, title):
	data = {
		"recipient": {"id": user_id},
        "message": {"attachment": {
        		"type":"template",
        		"payload":{
					"template_type":"generic",
					"elements":[{
						"title": title,
						"buttons":[{
							"type":"postback",
							"title":"Yes",
							"payload":"yes"
						},{
							"type":"postback",
							"title":"No",
							"payload":"no"
						}]
					}]
				}
        	}
        }
	}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAAb3lzmGmJcBAPTUWrJtcsGTzoHhVHzWpwUbXTHFLZBKJ79XDKZCLflSEkesDeNEcQOOF71Ru1dhvvignYf7Pza7SYxKIhCmMxOF84QrTZAa8igyNp3zCXM3ZC0O8CLS5kx73DZBgZAO4hjrF4ZB96qYWDN6EeUd4QGUGxaHxmdFgZDZD", json=data)
	print(resp)

def fb_render(user_id):
	data = {
		"recipient": {"id": user_id},
        "message": {"attachment": {
        		"type":"template",
        		"payload":{
					"template_type":"generic",
					"elements":[{
						"title": 'Confirm transfer',
						"buttons":[{
							"type":"web_url",
                    		"url":"https://9a2a2130.ngrok.io/mpin/",
                    		"title":"Yes",
                    		"webview_height_ratio": "compact",
                    		"messenger_extensions": "true"
						},{
							"type":"postback",
							"title":"No",
							"payload":"no"
						}]
					}]
				}
        	}
        }
	}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAAb3lzmGmJcBAPTUWrJtcsGTzoHhVHzWpwUbXTHFLZBKJ79XDKZCLflSEkesDeNEcQOOF71Ru1dhvvignYf7Pza7SYxKIhCmMxOF84QrTZAa8igyNp3zCXM3ZC0O8CLS5kx73DZBgZAO4hjrF4ZB96qYWDN6EeUd4QGUGxaHxmdFgZDZD", json=data)
	print(resp)

def fb_login_button(req, session_id):
	fb_login_template(req['originalRequest']['data']['sender']['id'])
	return "OK"

def send_money_initiate(req, session_id):
	fb_yes_no_template(req['originalRequest']['data']['sender']['id'], "Do you mean Mr.Prasanna Kumar")
	return "OK"

def transfer_money(req, session_id):
	r.hset("fizan", "amount", req.get('result').get('parameters').get('number'))
	fb_render(req['originalRequest']['data']['sender']['id'])
	return "OK"

actions = {
	"fb_login_button": fb_login_button,
	"send_money_initiate": send_money_initiate,
	"transfer_money": transfer_money
}

def process_request(req):
	if req.get("result") is None:
		return {}
	session_id = req.get("sessionId")
	action = req.get("result").get("action")
	print(action)
	if action in actions:
		return actions[action](req, session_id)
	else:
		return {}
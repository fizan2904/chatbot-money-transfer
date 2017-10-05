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
						"url": "https://12413345.ngrok.io/authorize"
					}]
				}
        	}
        }
    }
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAABslWK2vNkBALZCnljqesrwGaOciNYiq2WWzSneyCxkN1xW7MNBLZC2QCMSPSs0zqX867zXE4ZBYgdHo7gcsUIKa6KHci1p9Y2nW8mfanv7g97fyjTUKGRrBXFFX0cZBnQVW7MNs3euatIhw7ndpZBemosNDa6kj27qUAVt4zwZDZD", json=data)
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
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAABslWK2vNkBALZCnljqesrwGaOciNYiq2WWzSneyCxkN1xW7MNBLZC2QCMSPSs0zqX867zXE4ZBYgdHo7gcsUIKa6KHci1p9Y2nW8mfanv7g97fyjTUKGRrBXFFX0cZBnQVW7MNs3euatIhw7ndpZBemosNDa6kj27qUAVt4zwZDZD", json=data)
	print(resp)

def fb_login_button(req, session_id):
	fb_login_template(req['originalRequest']['data']['sender']['id'])
	return "OK"

def send_money_initiate(req, session_id):
	fb_yes_no_template(req['originalRequest']['data']['sender']['id'], "Select an option")
	return "OK"

def transfer_money(req, session_id):
	r.hset("fizan", "amount", req.get('result').get('parameters').get('number'))
	fb_yes_no_template(req['originalRequest']['data']['sender']['id'], "Confirm transfer")
	return "OK"

def confirm_transfer(req, session_id):
	return render_template('./mpin.html')

actions = {
	"fb_login_button": fb_login_button,
	"send_money_initiate": send_money_initiate,
	"transfer_money": transfer_money,
	"confirm_transfer": confirm_transfer
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
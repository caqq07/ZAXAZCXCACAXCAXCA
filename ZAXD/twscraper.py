import json
import os
import platform
import re
import sys
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests_oauthlib import OAuth1

import time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def login():
	try:
		t = str(getToken())
		headers={
			'X-Guest-Token': t,
			'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F'
		}
		return requests.get("https://api.twitter.com/1.1/search/tweets.json?q=bitcoin&lang=en&result_type=recent&f=live",headers=headers, verify=False)
	except Exception as e:
		print("Login func",e)
		return "false"


def getToken():
	page = ''
	while page == '':
		try:
			headers = {
				"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F"
			}
			guest_token = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers=headers, verify=False).json()['guest_token']
			return guest_token
		except Exception as e:
			time.sleep(5)
			continue


def getFollowers(xtoken, xsecret, username, cursor="-1"):
	try:
		headers = {
			"User-Agent": "Twitter-iPhone/9.62 iOS/13.3.3 (Apple;iPhone9,1;;;;;1)",
			"Content-Type": "application/json"
		}
		return requests.get("https://api.twitter.com/1.1/followers/list.json?cursor=" + str(cursor) + "&screen_name=" + str(username) + "&skip_status=true&include_user_entities=false&count=200", headers=headers, auth=OAuth1('3nVuSoBZnx6U4vzUxf5w', 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys', xtoken, xsecret, decoding=None), verify=False).json()
	except Exception as e:
		print("getFollowers func", e)


while True:
    for i in login().json()['statuses']:
        print(i['text'][:50])
    time.sleep(5)

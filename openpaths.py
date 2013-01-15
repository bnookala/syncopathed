#!/usr/bin/env python

import json
import oauth2
import time
import urllib
import urllib2

import config

API_PATH = "https://openpaths.cc/api/"
API_VERSION = 1
API_BASE_PATH = API_PATH + str(API_VERSION)

def build_auth_header(url, method):
	params = {
		'oauth_version': "1.0",
		'oauth_nonce': oauth2.generate_nonce(),
		'oauth_timestamp': int(time.time()),
	}
	consumer = oauth2.Consumer(key=config.ACCESS_KEY, secret=config.SECRET_KEY)
	params['oauth_consumer_key'] = consumer.key
	request = oauth2.Request(method=method, url=url, parameters=params)
	signature_method = oauth2.SignatureMethod_HMAC_SHA1()
	request.sign_request(signature_method, consumer, None)
	return request.to_header()

def get_points(start_time=None, end_time=None, num_points=2000):
	params = {}
	now = time.time()

	if start_time:
		params['start_time'] = start_time

	if end_time:
		params['end_time'] = end_time
	else:
		params['end_time'] = now

	if num_points:
		params['num_points'] = num_points

	query = "%s?%s" % (API_BASE_PATH, urllib.urlencode(params))

	request = urllib2.Request(query)
	request.headers = build_auth_header(API_BASE_PATH, 'GET')
	connection = urllib2.urlopen(request)
	data = json.loads(''.join(connection.readlines()))
	return data

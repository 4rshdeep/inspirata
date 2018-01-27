# -*- coding: utf-8 -*-

import json
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import requests
import urllib3
import os

LOCATION = "southcentralus"
URL = LOCATION + ".api.cognitive.microsoft.com"
APIKEY=os.environ['TEXT_API_KEY']


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#export environment variables
# http_proxy  = os.environ['http_proxy']
# https_proxy  = os.environ['https_proxy']
# ftp_proxy   = os.environ['http_proxy']

# proxyDict = {
#               "http"  : http_proxy,
#               "https" : https_proxy,
#               "ftp"   : ftp_proxy
#             }

def get_sentiment_val(data):
    # return data['documents']['score']
    return json.loads(data)['documents'][0]['score']
        


def get_sentiment(text):
    '''Gets the sentiments for a text and returns the information.'''
    
    ## TODO CHECK IF LANGUAGE IS ENGLISH USING APIs
    documents = {   
            'documents': [
        {'id': '1', 'language': 'en',
            'text': '-'}
    ]}

    documents['documents'][0]['text'] = text
    # Request headers    
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': APIKEY,
    }
    
    body = json.dumps(documents)
    
    params = urllib.parse.urlencode({ })
    
    try:
    	ENDPOINT = "https://"+URL+"/text/analytics/v2.0/sentiment?%s" % params
    	data = requests.post(ENDPOINT, headers = headers, data = body, verify=False)#, proxies=proxyDict)
        

    	return get_sentiment_val(data.text)
        # conn = http.client.HTTPSConnection(URL)
        # conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, str(body), headers)
        # response = conn.getresponse()
        # data = response.read().decode('utf-8')
        # return data
        # conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # data = requests.post("https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/semtiment", headers = headers, data = body, verify=False)
    # return data.text

# documents = {	
# 		'documents': [
#     {'id': '1', 'language': 'en',
#         'text': 'I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable.'},
#     {'id': '2', 'language': 'en',
#         'text': 'I am very sad.'}
# ]}


# Testing functions
# print('Please wait a moment for the results to appear.\n')
# result = get_sentiment('I am very sad.')
# print(result)

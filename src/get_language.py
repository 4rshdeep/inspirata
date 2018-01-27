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
http_proxy  = os.environ['http_proxy']
https_proxy  = os.environ['https_proxy']
ftp_proxy   = os.environ['http_proxy']

proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "ftp"   : ftp_proxy
            }

def get_language_val(data):
    # return data['documents']['score']
    return json.loads(data)['documents'][0]['detectedLanguages'][0]['name'], json.loads(data)['documents'][0]['detectedLanguages'][0]['score']
        


def get_language(text):
    '''Gets the language for a text and returns the information.'''
    
    ## TODO CHECK IF LANGUAGE IS ENGLISH USING APIs
    documents = {   
            'documents': [
        {'id': '1',
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
        ENDPOINT = "https://"+URL+"/text/analytics/v2.0/languages?%s" % params
        data = requests.post(ENDPOINT, headers = headers, data = body, verify=False, proxies=proxyDict)
        # print(data.text)
        return get_language_val(data.text)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

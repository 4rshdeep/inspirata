# -*- coding: utf-8 -*-

import json
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import requests
import urllib3

LOCATION = "southcentralus"
URL = LOCATION + ".api.cognitive.microsoft.com"
apikey='dd955a5dc6104d8596a40362503f8d56'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http_proxy  = "http://proxy62.iitd.ac.in:3128"
https_proxy  = "https://proxy62.iitd.ac.in:3128"
ftp_proxy   = "http://proxy62.iitd.ac.in:3128"

proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "ftp"   : ftp_proxy
            }

def GetSentiment(documents):
    '''Gets the sentiments for a set of documents and returns the information.'''
    
    # Request headers    
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': apikey,
    }
    
    body = json.dumps(documents)
    
    params = urllib.parse.urlencode({ })
    
    try:
    	ENDPOINT = "https://"+URL+"/text/analytics/v2.0/sentiment?%s" % params
    	data = requests.post(ENDPOINT, headers = headers, data = body, verify=False, proxies=proxyDict)
    	return data.text
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

documents = {	
		'documents': [
    {'id': '1', 'language': 'en',
        'text': 'I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable.'},
    {'id': '2', 'language': 'es',
        'text': 'Este ha sido un dia terrible, llegué tarde al trabajo debido a un accidente automobilistico.'}
]}


print('Please wait a moment for the results to appear.\n')

result = GetSentiment(documents)
print(json.dumps(json.loads(result), indent=4))

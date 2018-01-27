import time 
import requests
import operator
import numpy as np
import urllib

params = urllib.parse.urlencode({ })
_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize?%s'%params
_key = '41374a4e7ecb47da9ecec3a6c886ccfa' #Here you have to paste your primary key
_maxNumRetries = 10


def processRequest( json, data, headers, params ):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """
    retries = 0
    result = None
    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429: 
            print(response)
            print( "Message: %s" % ( response.json()['error']['message'] ) )
            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 200 or response.status_code == 201:
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )
        break
    return result

def get_sentiment(path):
    with open(path, 'rb') as f:
        data = f.read()
    try:
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = _key
        headers['Content-Type'] = 'application/octet-stream'
        json = None
        params = None
        response = processRequest( json, data, headers, params )
        result = response[0]['scores']

        my_param = result['anger']+result['contempt']+result['disgust']+result['sadness'] +result['fear']

        max_key = 'sadness'
        for key in result.keys():
            if (result[key]>my_param) and (key!='neutral'):
                max_key = key


        return my_param, max_key
    except Exception as e:
        print(response)
        print("Error")

import os
dir_path='test/'
images = os.listdir('test')
for image in images:
    image = dir_path+image
    print(image, end=" ")
    print(get_sentiment(image))
    # os.remove(image)
    
# if result is not None:
    # Load the original image from disk
    
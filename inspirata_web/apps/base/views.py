"""Views for the base app"""

from django.shortcuts import render, redirect
# from . import index
# from .index import MyListener
import os
import sys
################ index.py
import time, os
import json
from  configparser import *
import markovify
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import requests
import urllib3
import os
###############

LOCATION = "southcentralus"
URL = LOCATION + ".api.cognitive.microsoft.com"
APIKEY=os.environ['TEXT_API_KEY']

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)





###################
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
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

#############################

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
        data = requests.post(ENDPOINT, headers = headers, data = body, verify=False)#, proxies=proxyDict)
        print(data.text)
        return get_language_val(data.text)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


should_i_go_on=False


class MyListener(StreamListener):
    def on_data(self, data):
        if not (should_i_go_on):
            return False
            
        try:

            maintain_log = {}
            tweet_data = json.loads(data)
            tweet = tweet_data['text'].replace('RT ', '')
            tweet_id = str(tweet_data['id'])
            user_id = str(tweet_data['user']['id'])
            maintain_log['tweet'] = tweet

            # if p == 1:
            user = json.loads(data)['user']['screen_name']

            status = "@" + user + " " + text_model.make_short_sentence(138 - len(user))
            maintain_log['response'] = status

            logfile = open("logfile.txt", 'a')
            

            print('----------'*5)
            print("tweet: " + maintain_log['tweet'])

            # detect the language of the tweet
            tweet_language, tweet_language_score = get_language(maintain_log['tweet'])

            if tweet_language_score<0.80 or tweet_language != "English":
                logfile.write("tweet: " + maintain_log['tweet'])
                logfile.write("NR :: language :: "+str(tweet_language_score) + "response:: " + maintain_log['response'])
                print("NR :: language_score_is_low :: "+str(tweet_language_score))
                return True

            tweet_sentiment = get_sentiment(maintain_log['tweet'])
            response_sentiment = get_sentiment(maintain_log['response'])
            
            if tweet_sentiment>0.75:
                logfile.write("tweet: " + maintain_log['tweet'])
                logfile.write("NR :: tweet_sentiment_is_high :: " + str(tweet_sentiment))
                print("NR :: tweet_sentiment_is_high ::" + str(tweet_sentiment)) 
                return True

            
            if response_sentiment < 0.65:
                logfile.write("tweet: " + maintain_log['tweet'])
                logfile.write("NR :: sentiment :: "+str(response_sentiment) + "response:: " + maintain_log['response'])
                print("NR :: response_sentiment_is_low :: "+str(response_sentiment))
                return True

            
            print("response: " + maintain_log['response'])
            print('----------'*5)
            

            api.update_status(maintain_log['response'] +"  https://twitter.com/"+user_id+"/status/"+tweet_id)

            time.sleep(10)
            
        except BaseException as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return True

    def on_error(self, status):
        print(status)
        return True

###################################
def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')


def tweets(request):
    return render(request, 'base/tweets.html')

def start(request):
    if request.user.is_authenticated:
        should_i_go_on=True
        
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['ACCESS_SECRET']
    auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'enco.txt')
    # Train Markov Chain
    with open(file_path) as f:
       text = f.read()
       text_model = markovify.Text(text)
   
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=['anxiety', 'sadness', 'suicide', 'depression', 'sad'])


    if should_i_go_on:
        print("go_on")
    else:
        print("stop it")
        # os.system("sh environment.sh")

        # print("is_authenticated")
        # return redirect('home')#render(request, 'base/home.html')
    # else:
    return redirect('home') #render(request, 'base/home.html')


def stop(request):
    should_i_go_on=False
    if should_i_go_on:
        print("go_on")
    else:
        print("stop it")

    if request.user.is_authenticated:
        print("is_authenticated")
    else:
        print("Not authenticated")

    return render(request, 'base/home.html')

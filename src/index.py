import time, os
import json
from  configparser import *
import markovify
from sentiment_analysis import get_sentiment, get_sentiment_val
from get_language import get_language, get_language_val
from random import randint
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

# Train Markov Chain
with open('encouraging.txt') as f:
    text = f.read()
    text_model = markovify.Text(text)
    # text_model = POSifiedText(text)

class MyListener(StreamListener):
    def on_data(self, data):
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

            # logfile = open("logfile.txt", 'a')
            

            print('----------'*5)
            print("tweet: " + maintain_log['tweet'])

            # detect the language of the tweet
            tweet_language, tweet_language_score = get_language(maintain_log['tweet'])

            if tweet_language_score<0.80 or tweet_language != "English":
                # logfile.write("tweet: " + maintain_log['tweet'])
                # logfile.write("NR :: language :: "+str(tweet_language_score) + "response:: " + maintain_log['response'])
                print("NR :: language_score_is_low :: "+str(tweet_language_score))
                return True

            tweet_sentiment = get_sentiment(maintain_log['tweet'])
            response_sentiment = get_sentiment(maintain_log['response'])
            
            if tweet_sentiment>0.75:
                # logfile.write("tweet: " + maintain_log['tweet'])
                # logfile.write("NR :: tweet_sentiment_is_high :: " + str(tweet_sentiment))
                print("NR :: tweet_sentiment_is_high ::" + str(tweet_sentiment)) 
                return True

            
            if response_sentiment < 0.65:
                # logfile.write("tweet: " + maintain_log['tweet'])
                # logfile.write("NR :: sentiment :: "+str(response_sentiment) + "response:: " + maintain_log['response'])
                print("NR :: response_sentiment_is_low :: "+str(response_sentiment))
                return True

            
            print("response: " + maintain_log['response'])
            print('----------'*5)
            

            api.update_status(maintain_log['response'] +"  https://twitter.com/"+user_id+"/status/"+tweet_id)

            time.sleep(1200+randint(0, 600))
            
        except BaseException as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return True

    def on_error(self, status):
        print(status)
        return True
while(True):
    try:
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=['anxiety', 'sadness', 'suicide', 'depression', 'sad'])
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        f = open("tweepy_error_log.txt", 'a')
        f.write(time.strftime('Exception on Date: %Y-%m-%d Time: %H-%M-%S \n'))
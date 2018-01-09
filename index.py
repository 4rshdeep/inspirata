import time, os
import json
from  configparser import *
import markovify
from sentiment_analysis import get_sentiment, get_sentiment_val
# from bs4 import BeautifulSoup

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

# import nltk
# import re

# class POSifiedText(markovify.Text):
#     def word_split(self, sentence):
#         words = re.split(self.word_split_pattern, sentence)
#         words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
#         return words

#     def word_join(self, words):
#         sentence = " ".join(word.split("::")[0] for word in words)
#         return sentence


# Train Markov Chain
with open('enco.txt') as f:
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


            # file = open("tweet.json", 'a')
            # file.write(json.dumps(json.loads(data), indent=4))
            

            # reviews = []
            # texts = []
            # text = BeautifulSoup(tweet)
            # text = clean_str(text.get_text().encode('ascii','ignore'))
            # texts.append(text)
            # sentences = tokenize.sent_tokenize(text)
            # reviews.append(sentences)

            # tokenizer = Tokenizer(nb_words=MAX_NB_WORDS)
            # tokenizer.fit_on_texts(texts)

            # data = np.zeros((len(texts), MAX_SENTS, MAX_SENT_LENGTH), dtype='int32')

            # for i, sentences in enumerate(reviews):
            #     for j, sent in enumerate(sentences):
            #         if j< MAX_SENTS:
            #             wordTokens = text_to_word_sequence(sent)
            #             k=0
            #             for _, word in enumerate(wordTokens):
            #                 if k<MAX_SENT_LENGTH and tokenizer.word_index[word]<MAX_NB_WORDS:
            #                     data[i,j,k] = tokenizer.word_index[word]
            #                     k=k+1                    
                                
            # word_index = tokenizer.word_index
            # print('Total %s unique tokens.' % len(word_index))

            # print('Shape of data tensor:', data.shape)

            # indices = np.arange(data.shape[0])
            # np.random.shuffle(indices)
            # data = data[indices]
            # p = range(0, 2).index(max(loaded_model.predict(data)))

            # if p == 1:
            user = json.loads(data)['user']['screen_name']

            status = "@" + user + " " + text_model.make_short_sentence(138 - len(user))
            maintain_log['response'] = status

            logfile = open("logfile.txt", 'a')
            

            print('----------'*5)
            print("tweet: " + maintain_log['tweet'])
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

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['anxiety', 'sadness', 'suicide', 'depression', 'sad'])
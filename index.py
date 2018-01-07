import time, os
import json
from  configparser import *
import markovify
from sentiment_analysis import get_sentiment, get_sentiment_val
from get_language import get_language, get_language_val
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


# Train Markov Chain
with open('encouraging.txt') as f:
    text = f.read()
text_model = markovify.Text(text)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            maintain_log = {}
            tweet = json.loads(data)['text'].replace('RT ', '')
            
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
            

            api.update_status("@" + user + " " + text_model.make_short_sentence(138 - len(user)))
            time.sleep(180)
            
        except BaseException as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['anxiety', 'sadness', 'suicide', 'depression', 'sad'])
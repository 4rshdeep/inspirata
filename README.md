# [Inspirata](http://www.cse.iitd.ac.in/~cs5160625/cfd.html)
![inspirata](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/inspirata.jpg)

### Inspiring Lives.  
### From the people. For the people.  
Inspirata is a crowdsourced platform, which extracts motivating and encouraging tweets from Twitter and uses them to train a Markov Chain to produce encouraging words for those who might show signs of depression, suicide, anxiety etc.  
Responses generated by Inspirata can be seen [here](http://www.cse.iitd.ac.in/~cs5160625/cfd.html) and also on [Twitter](https://twitter.com/_inspirata/with_replies) and program is running on a local server.

# Specs
We used Microsoft Text Analytics APIs for Natural Language Processing and then use a markov chains to produce sentences. We first use Language Detection to segregate tweets in English. Sentiment analysis then calculates positive or negative sentiment which is used to classify the tweet as sad or happy. If the tweet is a sad one, our app replies the person who tweeted with an inspiring qoute. If the tweet is a happy one, our app uses it to train the Markov chain model for generating inspiring quotes to tweet. In this sense, our app is a crowdsourced app. 

### We are not using any hardcoded quotes. All the quotes are generated through Markov Chain.

# Demo
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/1.PNG)
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/7.PNG)
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/3.PNG)
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/4.PNG)

# Response
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/11.PNG)
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/10.PNG)
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/7.PNG)
![alt text](https://raw.githubusercontent.com/4rshdeep/Code.fun.do/master/images/6.PNG)

# Other:
Currently inspirata updates a tweet with a 20-30 minute interval.

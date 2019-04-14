import luigi
from TweetObject import TweetObject
import tweepy
from dateutil import parser
import time
import os
from StreamListener import Streamlistener

from dotenv import load_dotenv
load_dotenv(verbose=True)

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

class DataExtraction(luigi.Task):
	def requires(self):
		return []
 
	def output(self):
		return MockFile("DataExtraction", mirror_on_stderr=True)
 
	def run(self):
		# authentification so we can access twitter
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api =tweepy.API(auth, wait_on_rate_limit=True)
		# create instance of Streamlistener
		listener = Streamlistener(api=api)
		stream = tweepy.Stream(auth, listener = listener)

		track = ['golf', 'masters', 'reed', 'mcilroy', 'woods']
		# choose what we want to filter by
		stream.filter(track=track, languages=['en'])


class Analysis(luigi.task):
	def requires(self):
		return []
 
	def output(self):
		return MockFile("Analysis", mirror_on_stderr=True)
 
	def run(self):
		t = TweetObject(host='localhost', database='twitterdb', user='root')

	data  = t.connect("SELECT created_at, tweet FROM `TwitterDB`.`Golf`;")
	data = t.clean_tweets(data)
	data['Sentiment'] = np.array([t.sentiment(x) for x in data['clean_tweets']])
	t.word_cloud(data)
	t.save_to_csv(data)
	
	pos_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] > 0]
	neg_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] < 0]
	neu_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] == 0]

	#Print results
	print("percentage of positive tweets: {}%".format(100*(len(pos_tweets)/len(data['clean_tweets']))))
	print("percentage of negative tweets: {}%".format(100*(len(neg_tweets)/len(data['clean_tweets']))))
	print("percentage of neutral tweets: {}%".format(100*(len(neu_tweets)/len(data['clean_tweets']))))


if __name__ == '__main__':
	luigi.run()

	
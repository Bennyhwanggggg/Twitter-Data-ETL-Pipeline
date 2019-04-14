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


if __name__== '__main__':

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



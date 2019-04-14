import mysql.connector
from mysql.connector import Error
import tweepy
import json
from dateutil import parser
import time
import os
import subprocess
from StreamListener import Streamlistener

from dotenv import load_dotenv
load_dotenv(verbose=True)

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
password = os.environ['PASSWORD']


def connect(username, created_at, tweet, retweet_count, place , location):
	"""
	connect to MySQL database and insert twitter data
	"""
	try:
		con = mysql.connector.connect(host = 'localhost',
		database='twitterdb', user='root', password = password, charset = 'utf8')
		

		if con.is_connected():
			"""
			Insert twitter data
			"""
			cursor = con.cursor()
			# twitter, golf
			query = "INSERT INTO Golf (username, created_at, tweet, retweet_count,place, location) VALUES (%s, %s, %s, %s, %s, %s)"
			cursor.execute(query, (username, created_at, tweet, retweet_count, place, location))
			con.commit()
			
			
	except Error as e:
		print(e)

	cursor.close()
	con.close()

	return



if __name__== '__main__':
	print(consumer_key, consumer_secret)

	# # #Allow user input
	# track = []
	# while True:

	# 	input1  = input("what do you want to collect tweets on?: ")
	# 	track.append(input1)

	# 	input2 = input("Do you wish to enter another word? y/n ")
	# 	if input2 == 'n' or input2 == 'N':
	# 		break
	
	# print("You want to search for {}".format(track))
	# print("Initialising Connection to Twitter API....")
	# time.sleep(2)

	# authentification so we can access twitter
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api =tweepy.API(auth, wait_on_rate_limit=True)

	# create instance of Streamlistener
	listener = Streamlistener(api = api)
	stream = tweepy.Stream(auth, listener = listener)

	track = ['golf', 'masters', 'reed', 'mcilroy', 'woods']
	#track = ['nba', 'cavs', 'celtics', 'basketball']
	# choose what we want to filter by
	stream.filter(track = track, languages = ['en'])
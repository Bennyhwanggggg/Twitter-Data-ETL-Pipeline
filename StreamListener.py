import tweepy
import mysql.connector
from mysql.connector import Error
from dateutil import parser
import os
import json

from dotenv import load_dotenv
load_dotenv(verbose=True)

password = os.environ['PASSWORD']

# Tweepy class to access Twitter API
class Streamlistener(tweepy.StreamListener):
	
	def on_connect(self):
		print("You are connected to the Twitter API")

	def on_error(self):
		if status_code != 200:
			return False

	def on_data(self,data):
		"""Read in tweet data as json and do extraction
		"""
		try:
			raw_data = json.loads(data)

			if 'text' in raw_data:
				# Get all data
				username = raw_data['user']['screen_name']
				created_at = parser.parse(raw_data['created_at'])
				tweet = raw_data['text']
				retweet_count = raw_data['retweet_count']
				place = raw_data['place']['country'] if raw_data['place'] is not None else None
				location = raw_data['user']['location']
				#insert data just collected into MySQL database
				self.connect(username, created_at, tweet, retweet_count, place, location)
				print("Tweet colleted at: {} ".format(str(created_at)))
		except Error as e:
			'Error collecting tweet data: {}'.format(e)

	def connect(self, username, created_at, tweet, retweet_count, place , location):
		"""Connect to MySQL database and insert twitter data
		"""
		cursor, con = None, None
		try:
			con = mysql.connector.connect(host='localhost',
																		database='twitterdb', 
																		user='root', 
																		password=password, 
																		charset='utf8',
																		auth_plugin='mysql_native_password')
			if con.is_connected():
				cursor = con.cursor()
				query = "INSERT INTO Golf (username, created_at, tweet, retweet_count,place, location) VALUES (%s, %s, %s, %s, %s, %s)"
				cursor.execute(query, (username, created_at, tweet, retweet_count, place, location))
				con.commit()
				print('Data upload soccess.')
		except Error as e:
			print('Error uploading data: {}'.format(e))
		if cursor:
			cursor.close()
		if con:
			con.close()


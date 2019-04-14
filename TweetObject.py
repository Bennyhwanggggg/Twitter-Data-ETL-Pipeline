import mysql.connector 
from mysql.connector import Error
import os
import re
import pandas as pd 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob

from dotenv import load_dotenv
load_dotenv(verbose=True)


class TweetObject:
	def __init__(self, host, database, user):
		self.password = os.environ['PASSWORD']
		self.host = host
		self.database = database
		self.user = user
		
	def connect(self, query):
		"""Connects to database and extracts raw tweets and any other columns we
		need
		"""
		try:
			con = mysql.connector.connect(host=self.host, 
																		database=self.database,
																		user=self.user, 
																		password=self.password, 
																		charset='utf8')
			if con.is_connected():
				print("Successfully connected to database")
				cursor = con.cursor()
				query = query
				cursor.execute(query)
				data = cursor.fetchall()
				# store in dataframe
				df = pd.DataFrame(data,columns = ['date', 'tweet'])
				print('Query executed successfully')
		except Error as e:
			print(e)
		
		cursor.close()
		con.close()
		return df

	def clean_tweets(self, df):
		"""Preprocess raw tweets by removing stopwards, punctuation, lowercase and emoticons
		"""
		stopword_list = stopwords.words('english')
		ps = PorterStemmer()
		df["clean_tweets"], df['len'] = None, None
		for i in range(0,len(df['tweet'])):
			# get rid of anythin that isnt a letter
			exclusion_list = ['[^a-zA-Z]','rt', 'http', 'co', 'RT']
			exclusions = '|'.join(exclusion_list)
			text = re.sub(exclusions, ' ' , df['tweet'][i])
			text = text.lower()
			words = text.split()
			words = [word for word in words if not word in stopword_list]
			df['clean_tweets'][i] = ' '.join(words)
		# Create column with data length
		df['len'] = np.array([len(tweet) for tweet in data["clean_tweets"]])
		return df

	def sentiment(self, tweet):
		"""Sentimental analysis of tweets. 
		"""
		analysis = TextBlob(tweet)
		if analysis.sentiment.polarity > 0:
			return 1
		elif analysis.sentiment.polarity == 0:
			return 0
		else:
			return -1

	def save_to_csv(self, df):
		"""Save dataframe into csv
		"""
		try:
			df.to_csv("clean_tweets.csv")
			print("\n")
			print("csv successfully saved. \n")
		except Error as e:
			print(e)
		
	def word_cloud(self, df):
		"""Plot word cloud
		"""
		plt.subplots(figsize = (12,10))
		wordcloud = WordCloud(
				background_color = 'white',
				width = 1000,
				height = 800).generate(" ".join(df['clean_tweets']))
		plt.imshow(wordcloud)
		plt.axis('off')
		plt.show()
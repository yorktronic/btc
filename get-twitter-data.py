import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from string import punctuation
import csv

def cleanTweets(csv_file_name):
	df = pd.read_csv(csv_file_name)
	junk = re.compile("al|RT|\n|&.*?;|http[s](?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)*")
	names = ['hillary', 'trump', 'cruz', 'bernie', 'sanders', 'ted']
	tweets = [junk.sub(" ", s) for s in df.text]
	
	return tweets

def createWordCloud(tweets):
	vec = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=.5)
	tfv = vec.fit_transform(tweets)
	terms = vec.get_feature_names()
	wc = WordCloud(height=1000, width=1000, max_words=1000).generate(" ".join(terms))

	return wc

def visualizeWordCloud(wc):
	plt.figure(figsize=(10,10))
	plt.imshow(wc)
	plt.axis("off")
	plt.show()

def doIt(csv_file_name):
	tweets = cleanTweets(csv_file_name)
	wc = createWordCloud(tweets)
	visualizeWordCloud(wc)

doIt('./realDonaldTrump_tweets.csv')
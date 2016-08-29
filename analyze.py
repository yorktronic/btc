#####################################################################################################################
#
# Analyses of tweets, including building word clouds, analyzing sentiment, and generating fake Donald Trump tweets
#
#####################################################################################################################

import getandclean as gc
import matplotlib as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import pandas as pd
import json

def getCleanTwitterData(acct_names):
    # Takes in a list of account names and pulls the last 3240 tweepy Status objects for all provided account names
    # Returns a dictionary where the account names as keys and a list of tweepy Status objects as values
    tweets_all_accounts = {}
    for name in acct_names:
        print "getting tweets for screen name {}".format(name)
        tweets = gc.getTweets(name)

        for tweet in tweets:
            tweet.text = gc.cleanTweet(tweet.text)

        tweets_all_accounts['name'] = tweets

    return tweets_all_accounts

# TODO: get subscriber counts
# TODO: repurpose this to handle pulling from json and from Status objects?
def toDataframe(tweets_all_accounts):
    # Takes in a dictionary with keys as account names and values a list of tweepy Status objects
    # Returns a DataFrame with all tweets

    # Get a list of the account names we're working with in case we need them
    acct_names = tweets_all_accounts.keys()

    # Map dataframe columns to tweepy Status object structure
    mapping = {'tweetID': 'id', 'author': 'author', 'retweeted': 'retweeted', 'retweet_count': 'retweet_count',
               'user': 'user', 'created_at': 'date'}

    df = pd.DataFrame(columns=mapping.keys())

    # TODO: get the attirbutes of the Object and use the provided info to create columns, rather than manually doing so
    for name in acct_names:
        # For each user, populate df with tweets
        tweets = tweets_all_accounts[name]
        for tweet in tweets:
            df['id'] = tweet.id
            df['author'] = tweet.author
            df['retweeted'] = tweet.retweeted
            df['retweet_count'] = tweet.retweet_count
            df['user'] = tweet.user
            df['date'] = tweet.created_at

    return df

def createWordCloud(tweets):
    vec = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=.5)
    tfv = vec.fit_transform(tweets)
    terms = vec.get_feature_names()
    wc = WordCloud(height=1000, width=1000, max_words=300).generate(" ".join(terms))

    return wc

def visualizeWordCloud(wc):
    plt.figure(figsize=(10,10))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

def doIt(tweets):
    wc = createWordCloud(tweets.text)
    visualizeWordCloud(wc)
#####################################################################################################################
#
# Data retrieval and cleaning script for pulling tweets via Twitter's API
#
#####################################################################################################################

import tweepy
import credentials
from tweepy import OAuthHandler
import json

consumer_key = credentials.twitter_consumer_key
consumer_secret = credentials.twitter_consumer_secret
access_token = credentials.twitter_access_key
access_secret = credentials.twitter_access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

def getTweets(screen_name):
    # Gets the most recent 3240 tweets for a provided screen_name
    # List for holding tweets
    tweets = []

    # Get most recent 200 tweets
    new_tweets = api.user_timeline(screen_name = screen_name, count=200)

    # Save most recent tweets
    tweets.extend(new_tweets)

    # Save the id of the oldest tweet - 1
    oldest = tweets[-1].id - 1

    # Keep grabbing tweets until there are none left to grab
    while len(new_tweets) > 0:
        print "getting tweets before {}".format(oldest)

        # Use max_id param to prevent dupes
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # Save most recent tweets
        tweets.extend(new_tweets)

        # update the id of the oldest tweet - 1
        oldest = tweets[-1].id - 1

        print "...{} tweets by {} downloaded so far".format(len(tweets), screen_name)

    # Return all the tweets that can then be stored as CSV or JSON
    return tweets

def storeTweetsJson(tweets, screen_name, clean=False):
    # Takes in a list of tweet objects and the user's screen name and whether or not the tweet text has been cleaned
    # Stores them in a JSON-formatted text file

    outTweets = []
    for tweet in tweets:
        outTweets.append(tweet._json)

    # If the tweets are already cleaned, save them as screen_name_clean.txt
    if clean:
        with open('./data/{}_clean.json'.format(screen_name), 'w') as outFile:
            json.dump(outTweets, outFile)
    # Otherwise just save them with the screen_name
    else:
        with open('./data/{}.json'.format(screen_name), 'w') as outFile:
            json.dump(outTweets, outFile)

    print "...{} tweets by {} saved as {}".format(len(tweets), screen_name, outFile)

def cleanTweet(tweet):
    # Takes in string (the text from a tweet object) and returns a tokenized list of strings w/ stopwords removed

    import re

    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

    def tokenize(s):
        return tokens_re.findall(s)

    def preProcess(s, lowercase=False):
        tokens = tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    def removeStopwords(tokens):
        # Takes in list of tokenized strings and removes stopwords like "in," "an," etc
        from nltk.corpus import stopwords
        import string

        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['rt', 'via']
        terms_no_stopwords = [term for term in tokens if term not in stop]

        return terms_no_stopwords

    return removeStopwords(preProcess(tweet, lowercase=True))



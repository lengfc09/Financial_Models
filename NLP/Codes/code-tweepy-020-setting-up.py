# This script shows how you can set up your Twitter API login
# information. 
import tweepy

# Alternatively you can load your keys from a separate text file,
# e.g. `exec(open('../code-API-key-tweepy.py').read())`.
access_token = "..."
access_token_secret = "..."
consumer_key = "..."
consumer_secret = "..."

auth = tweepy.OAuthHandler(access_token, access_token_secret)
auth.set_access_token(consumer_key, consumer_secret)
api = tweepy.API(auth)

# Check the tweets in your stream.
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


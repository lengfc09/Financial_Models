# This script listens on the Twitter stream for the keyword 'python'
# and prints select fields from each tweet, such as name, follower
# count, date, and the tweet itself.
import tweepy

# Set up Twitter API. Alternatively you can load your keys from a
# separate text file,
# e.g. `exec(open('../code-API-key-tweepy.py').read())`.
access_token = "..."
access_token_secret = "..."
consumer_key = "..."
consumer_secret = "..."

auth = tweepy.OAuthHandler(access_token, access_token_secret)
auth.set_access_token(consumer_key, consumer_secret)
api = tweepy.API(auth)

# # Define subclass of `tweepy.StreamListener` to add logic to
# # `on_status`. This listener will print only the first 140 characters,
# # so will truncate any extended tweets (the ones with up to 280
# # characters).
# class listener(tweepy.StreamListener):
#     def on_status(self, status): # Overwrite `on_status` method.
#         print(
#             status.user.screen_name, ':',
#             status.user.followers_count, ':',
#             status.created_at, ':', # UTC time.
#             status.text)

# Define subclass of `tweepy.StreamListener` to add logic to
# `on_status`. See
# http://docs.tweepy.org/en/latest/extended_tweets.html.
class listener(tweepy.StreamListener):
    def on_status(self, status):
        print(
            status.user.screen_name, ':',
            status.user.followers_count, ':',
            status.created_at, ':')             # UTC time.
        if hasattr(status, 'retweeted_status'): # Check if it's a retweet.
            try:
                print(status.retweeted_status.extended_tweet['full_text'])
            except AttributeError:
                print(status.retweeted_status.text)
        else:
            try:
                print(status.extended_tweet['full_text'])
            except AttributeError:
                print(status.text)

# Create a Stream.
mystream = \
    tweepy.Stream(
        auth=api.auth,
        listener=listener())
# Start a Stream.
mystream.filter(track=['python'])

# This script listens to a keyword (e.g. 'python' in the example
# below) and writes the whole Twitter stream to a file.
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

class listener(tweepy.StreamListener):
    def on_data(self, data):    # Alternatively use `on_status`.
        with open('data-streaming-tweets.txt', 'a') as f:
            f.write(data)
        return True
    
    def on_error(self, status_code):
        print(status_code)

mystream = \
    tweepy.Stream(
        auth=api.auth,
        listener=listener())
mystream.filter(track=['python'])

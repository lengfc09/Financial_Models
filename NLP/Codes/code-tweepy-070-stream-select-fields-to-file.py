# This script shows how to stream only selected fields to a file. The
# fields are separated by ' : ' (i.e. space, colon, space) for easier
# parsing later on.
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
    def on_status(self, status):
        with open('data-streaming-tweets.txt', 'a') as f:
            f.write(
                status.user.screen_name + ' : ' + \
                str(status.user.followers_count) + ' : ' + \
                str(status.created_at) + ' : ' + \
                status.text + '\n')
        return True
    
    def on_error(self, status_code):
        print(status_code)

mystream = \
    tweepy.Stream(
        auth=api.auth,
        listener=listener())
mystream.filter(
    track=[
        '$SPX', '$SPY', '$ES',
        '$DJI', '$DJIA', '$INDU', '$YM',
        '$NQ', '$NASDAQ', '$QQQ',
        '$TLT',
        '$GC', '$GLD',
        '$NG', '$WTI'])

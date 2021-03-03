# Twitter only allows access to a users most recent 3240 tweets
# with this method.
import tweepy
import csv

# Twitter user you want to download.
screen_name = "StockCats"


# Here you need to specify your Twitter API login details. You can get
# the login details from the Twitter website.
#
# Here I read this API login information from another file, but for
# your purposes, you can specify them directly as in the commented-out
# code below.
exec(open('../code-API-key-tweepy.py').read())
# access_token = "..."
# access_token_secret = "..."
# consumer_key = "..."
# consumer_secret = "..."

# Authorize Twitter.
auth = tweepy.OAuthHandler(access_token, access_token_secret)
auth.set_access_token(consumer_key, consumer_secret)
api = tweepy.API(auth)
# Initialize a list to hold all the tweets.
alltweets = []	
# Make initial request for most recent tweets (200 is the maximum
# allowed count).
new_tweets = \
    api.user_timeline(
        screen_name = screen_name,
        count = 200)
# Save most recent tweets to the list.
alltweets.extend(new_tweets)
# Save the id of the oldest tweet less one.
oldest = alltweets[-1].id - 1
# Keep grabbing tweets until there are no tweets left to grab.
while len(new_tweets) > 0:
    print("getting tweets before %s" % oldest)
    # All subsequent requests use the max_id param to prevent
    # duplicates.
    new_tweets = \
        api.user_timeline(
            screen_name = screen_name,
            count = 200,
            max_id = oldest)
    # Save most recent tweets.
    alltweets.extend(new_tweets)
    # Update the id of the oldest tweet less one.
    oldest = alltweets[-1].id - 1
    print("...%s tweets downloaded so far" % len(alltweets))

# Use list comprehension to transform the tweets into a 2D array
# (list of row objects) that will populate the CSV file.
outtweets = \
    [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")]
     for tweet in alltweets]
# Write to CSV file.
with open('data-%s-tweets.csv' % screen_name, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "created_at", "text"])
    writer.writerows(outtweets)


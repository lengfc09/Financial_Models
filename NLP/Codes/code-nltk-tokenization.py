# This file shows some tokenization examples using the NLTK package.
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize, TweetTokenizer
word_tokenize("Hi there!")
sent_tokenize('Hello world. I love HK!')
# Make set of unique tokens.
set(word_tokenize('I love HK. I love NYC'))
# Tokenize based on regular expression.
regexp_tokenize('SOLDIER #1: Found them?', r'(\w+|#\d|\?|!)')
# Find hastags in tweets.
regexp_tokenize('This is a great #NLP exercise.', r'#\w+')
# Find mentions and hashtags.
regexp_tokenize('great #NLP exercise from @blabla.', r'[#@]\w+')
tknzr = TweetTokenizer()        # Create instance of TweetTokenizer.
[tknzr.tokenize(t) for t in ['thanks @blabla', '#NLP is fun!']]

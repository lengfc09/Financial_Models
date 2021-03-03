# Bag-of-words using gensim.
from gensim.corpora.dictionary import Dictionary
from nltk.tokenize import word_tokenize
# This is an example corpus consisting of movie reviews. You can think
# of each movie review as a separate text document.
cp = \
    ['The movie was about a spaceship and aliens. The movie is wonderful!',
     'I really liked the movie. More people should go see it.',
     'Awesome action scenes, but boring characters.']
# Create tokenized corpus. Very basic preprocessing. Usually you would
# do more work here.
cp = [word_tokenize(doc.lower()) for doc in cp]
cp = [[token for token in doc if token.isalnum() and len(token) > 1]
      for doc in cp]

# Pass to gensim `Dictionary` class. This assigns to each token
# (e.g. word) a unique integer ID. Later on we will just work with
# those IDs instead of the tokens directly because it is
# computationally easier to handle (there is a one-to-one mapping
# between both, so we are not losing any information). The reason why
# we use a dictionary is that it gives us a list of words we are
# interested in examining further. If a word is not in the dictionary
# but occurs in a document, it will be ignored by gensim.
d = Dictionary(cp)
d.token2id  # Like dict(d); show mapping between tokens and their IDs.
d.token2id.get('awesome')       # What's the ID for 'awesome'?
d.get(0)                        # Which token has ID=0?
d.dfs # In how many documents does each token appear? (Document frequency).

# For a single document, we can now calculate the token frequencies
# using the dictionary we just created. "Calculating token
# frequencies" means we're counting words.
d.doc2bow(cp[2])

# Next, using the dictionary we just created, we build a gensim
# corpus, which is just a bag-of-words representation of the original
# corpus. This is a nested list (a list of lists), where each list
# corresponds to a document. Inside each list we have tuples in the
# form
#
# (token_ID, token_frequency).
#
# So all we are really doing here is counting words.
cp = [d.doc2bow(doc) for doc in cp]
# This gensim corpus can now be saved, updated, and reused using tools
# from gensim. The dictionary can also be saved and updaed as well,
# e.g. if we need to add more words later on.

# Print the first three token IDs and their frequency counts from the
# first document.
cp[0][:3]
# For the first document, sort the tokens according to their
# frequency, with the most frequent tokens coming first.
sorted(
    cp[0],                 # First document.
    key = lambda x: x[1],  # Sort by token_frequency (second element).
    reverse = True)        # Most frequent first.

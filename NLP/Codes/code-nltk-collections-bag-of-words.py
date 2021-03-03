# This file shows simple examples how to calculate bag-of-words.
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
text = '''The cat is in the box.
          The cat likes the box.
          The box is over the cat.'''
# Simple example without any preprocessing.
c = Counter(word_tokenize(text))
c                               # View the counts.
c.values()                      # Only the word count numbers.
c.most_common(2)                # The two most common words.
list(c.elements())              # All the words.
# Convert to lowercase and only keep alphabetic (remove punctuation etc.)
tokens = [w for w in word_tokenize(text.lower()) if w.isalpha()]
# Keep words that are not stopwords (i.e. remove stopwords).
no_stops = [t for t in tokens if t not in stopwords.words('english')]
Counter(no_stops).most_common(2)
# Now we lemmatize the words (similar to stemming).
wnl = WordNetLemmatizer()
lemmatized = [wnl.lemmatize(t) for t in no_stops]
Counter(lemmatized).most_common(2)

# An alternative that is native to NLTK but actually an extension of
# the `Counter` class. Another advantage is that it can plot easily
# using the matplotlib package.
from nltk.probability import FreqDist
fd = FreqDist(lemmatized)
fd                           # Looks like `Counter`.
fd.plot(10)                  # Specify how many words to plot at most.

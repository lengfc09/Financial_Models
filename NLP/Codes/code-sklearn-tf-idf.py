# This code uses scikit-learn to calculate tf-idf. The code is very
# similar to the one used with `CountVectorizer` (which give BoW).
from sklearn.feature_extraction.text import TfidfVectorizer
# Vectorizer. `max_df` tells sklearn to ignore terms that have a
# document frequency higher than this threshold when building the
# vocabulary.
v = TfidfVectorizer(stop_words='english', max_df=0.9)
c = [                           # Minimal corpus for illustration.
    'This is the first document.',
    'This is the second document.',
    'And the third one.',
    'Is this the first document?',
]
# Learn the vocabulary dictionary and return the document-term
# matrix. Tokenize and count word occurrences.
tfidf = v.fit_transform(c)
# Each term found by the analyzer during the fit is assigned a unique
# integer index corresponding to a column in the resulting
# matrix. This interpretation of the columns can be retrieved as
# follows.
tfidf.toarray()                   # Print the document-term matrix.
tfidf.A                           # Same effect, shortcut command.
v.get_feature_names()           # Which term is in which column?
# Inverse mapping from feature name to column index.
v.vocabulary_.get('second')
# Mapping of documents to their tf-idf scores. Words that were not
# seen in the training corpus are ignored.
v.transform(['Something completely new.']).toarray()
v.transform(['A second try.']).toarray()

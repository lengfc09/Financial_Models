# This code uses scikit-learn to calculate bag-of-words
# (BOW). `CountVectorizer` implements both tokenization and occurrence
# counting in a single class.
from sklearn.feature_extraction.text import CountVectorizer
v = CountVectorizer(stop_words='english') # Vectorizer.
c = [                           # Minimal corpus for illustration.
    'This is the first document.',
    'This is the second document.',
    'And the third one.',
    'Is this the first document?',
]
# Learn the vocabulary dictionary and return the document-term
# matrix. Tokenize and count word occurrences.
bow = v.fit_transform(c)
# Each term found by the analyzer during the fit is assigned a unique
# integer index corresponding to a column in the resulting
# matrix. This interpretation of the columns can be retrieved as
# follows.
bow.toarray()                   # Print the document-term matrix.
bow.A                           # Same effect, shortcut command.
v.get_feature_names()           # Which term is in which column?
# Inverse mapping from feature name to column index.
v.vocabulary_.get('second')
# Mapping of documents to BOW. Words that were not seen in the
# training corpus are ignored.
v.transform(['Something completely new.']).toarray()
v.transform(['A second try.']).toarray()

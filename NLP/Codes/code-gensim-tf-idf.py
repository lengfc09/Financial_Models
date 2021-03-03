# This script illustrates how to use tf-idf with gensim.
from nltk.tokenize import word_tokenize
from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
corpus = ['The movie was about a spaceship and aliens. It is wonderful!',
          'I really liked the movie. More people should go see it.',
          'Awesome action scenes, but boring characters.']
tokenized_corpus = [word_tokenize(doc.lower()) for doc in corpus]
d = Dictionary(tokenized_corpus)
bowcorpus = [d.doc2bow(doc) for doc in tokenized_corpus]
# All the above steps are standard, but now it gets interesting:
tfidf = TfidfModel(bowcorpus) # Create new TfidfModel from BoW corpus.
tfidf_weights = tfidf[bowcorpus[0]] # Weights of first document.
tfidf_weights[:5]                   # First five weights (unordered).
 # Print top five weighted words.
sorted_tfidf_weights = \
    sorted(
        tfidf_weights,
        key=lambda x: x[1],
        reverse=True)
for term_id, weight in sorted_tfidf_weights[:5]:
    print(d.get(term_id), weight)

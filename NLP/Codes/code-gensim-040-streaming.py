# This script shows how to stream text documents using iterators. The
# key advantage is that we do not need to hold all the documents
# (i.e. the whole corpus) in memory. Instead, we process it chunk by
# chunk using iterators.
#
# In the first part, we show how to generate and modify a gensim
# `Dictionary` using iterators.
#
# In the second part, we show how to stream a corpus and calculate bag
# of words.
from gensim import corpora

# Construct dictionary WITHOUT loading all texts in memory. Instead,
# we chunk over the documents step by step using a generator
# expression. Once we're done with a document, the memory is freed.
dictionary = \
    corpora.Dictionary(
        line.lower().split() for line in open('data-gensim-mycorpus.txt'))

# Get the IDs in gensim that correspond to stopwords.
stoplist = set('for a of the and to in'.split())
stop_ids = \
    [dictionary.token2id[stopword] for stopword in stoplist
     if stopword in dictionary.token2id]

# Obtain the token IDs for words that appear only ONCE in the text
# corpus (these words will be removed later). `iteritems` from the six
# library is used here to iterate over the keys and values of the
# dictionary `dictionary.dfs` in a way that works both with Python 2
# and 3. (In Python 3 you would use `dictionary.dfs.items()`.)
# `dictionary.dfs` is a dict with the token ID and its document
# frequency (i.e. the frequency with which it occurs in the text
# corpus as a whole).
from six import iteritems
once_ids = \
    [tokenid for tokenid, docfreq in iteritems(dictionary.dfs)
     if docfreq == 1]

# Remove tokens that are stopwords or words that appear only once (or
# both).
dictionary.filter_tokens(stop_ids + once_ids)

# Remove gaps in ID sequence after words that were removed.
dictionary.compactify()

# Show how many words ("tokens") the dictionary contains, show their
# mappings to integer IDs, and show their document frequency (i.e. how
# often they appear in the text corpus).
print(dictionary)
print(dictionary.token2id)
print(dictionary.dfs)

# Using the `dictionary` created above, we can also stream a corpus
# into gensim and calculate BoW. Here we define the `__iter__()`
# method as a generator function. As a consequence, an instance of
# `MyCorpus` is an iterable. We iterate through a file under the
# assumption that each line holds one document. If this assumption is
# not satisfied (e.g. your file has a different format to hold the
# text documents), you can modify the definition of the `__iter__`
# method to fit your input format.
class MyCorpus(object):
    def __iter__(self):         # Define generator function.
        for line in open('data-gensim-mycorpus.txt'):
            yield dictionary.doc2bow(line.lower().split())

# Printing the corpus just shows the address of the object in
# memory. To see all the documents (represented as vectors using
# `doc2bow` above), we iterate over the corpus. The important thing is
# that only a SINGLE vector resides in memory at a time!
mycp = MyCorpus()      # Create iterable (by instantiating the class).
print(mycp)
for vector in mycp:
    print(vector)

# Another way to print a corpus is to load it entirely into memory.
print(list(mycp))

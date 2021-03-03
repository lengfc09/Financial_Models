# First we import from the module `gensim` the name `corpora`. This
# means the name`corpora` is directly imported into our symbol table.
from gensim import corpora

# Here we generate a text corpus as a list of strings. This corpus is
# held in memory, which is fine for us because the corpus is
# tiny. However, for larger corpora this could lead to problems.
documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

# We manually create a set of stopwords. This is of course not a
# comprehensive set, so in a real application you would use a set of
# stopwords for example from NLTK, SpaCy, or scikit-learn.
stoplist = set('for a of the and to in'.split())

# We iterate over all documents, convert each document to lowercase
# and tokenize each document (using a very simple tokenizer consisting
# of just splitting on whitespace). We then iterate over each word and
# check whether it is stopword (in which case it is removed).
texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in documents]



# Using the specialized container datatype `defaultdic` (which is a
# subclass of `dict` that is e.g.  useful for counting) from the
# `collections` module, we count how often each word ("token") appears
# in the text corpus.
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# We remove all words ("tokens") that appear less than twice in the
# corpus.
texts = [[token for token in text if frequency[token] >= 2] for text in texts]



# Here we use a dictionary to assign to each word a unique integer
# ID. If necessary, we can save it to a file for future reference.
dictionary = corpora.Dictionary(texts)
# dictionary.save('data-gensim-deerwester.dict')
print(dictionary)               # Show the number of distinct words.
print(dictionary.token2id)      # Show mapping between words and IDs.
print(dictionary.dfs) # Show document frequency of words in dictionary.

# `doc2bow` is the main function to convert a new document to a
# bag-of-words representation, i.e. counting each word. If a word
# (e.g. "interaction" below) is not in the dictionary, it is
# ignored. The function `doc2bow` returns a list of 2-tupels, each of
# the form (token_id,token_count).
dictionary.doc2bow("Human computer interaction".lower().split())

# We can now convert the whole text corpus to bag-of-words. If
# necessary, we can store it to disk for later use.
corpus = [dictionary.doc2bow(text) for text in texts]
# corpora.MmCorpus.serialize('data-gensim-deerwester.mm', corpus)
print(corpus)

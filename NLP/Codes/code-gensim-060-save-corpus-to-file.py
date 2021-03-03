from gensim import corpora

# Create a very simple corpus (just a list) consisting of two
# documents. The first document has one word with token ID of 1 and
# value of 0.5 while the second document is empty.
corpus = [[(1, 0.5)], []]

# Save corpus in Matrix Market format. This is a relatively popular
# format.
corpora.MmCorpus.serialize('data-gensim-corpus.mm', corpus)

# Save corpus in SVMlight format.
corpora.SvmLightCorpus.serialize('data-gensim-corpus.svmlight', corpus)

# Save corpus in Blei's LDA-c format.
corpora.BleiCorpus.serialize('data-gensim-corpus.lda-c', corpus)

# Save corpus in GibbsLDA++ format
corpora.LowCorpus.serialize('data-gensim-corpus.low', corpus)

# You can also read the corpus back into Python. Here you load a
# corpus iterable from a Matrix Market file. We then print it in a
# couple of different ways. The first way just shows some meta
# information about the corpus (after all, it's a stream). The second
# way loads it entirely into memory and prints it. The third way
# prints it one document at a time in a memory-friendly way.
corpus = corpora.MmCorpus('data-gensim-corpus.mm') # An iterable.
print(corpus)
print(list(corpus))
for doc in corpus:
    print(doc)

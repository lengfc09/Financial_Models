# This script illustrates how to use latent Dirichlet allocation (LDA)
# using the Gensim package. The data is a random extract from the
# English Wikipedia.

import logging, gensim
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

# Load the ID to word mapping, i.e. the dictionary. This has been done
# in a previous step, when preparing the corpus with
# `gensim.scripts.make_wiki`.
id2word = \
    gensim.corpora.Dictionary.load_from_text(
        '../data-wiki-en/wiki_en_wordids.txt.bz2')
# Load the corpus iterable.
mm = gensim.corpora.MmCorpus('../data-wiki-en/wiki_en_tfidf.mm')
# Take a look basic information about the corpus.
print(mm)

# Extract 100 LDA topics, using 1 pass and updating once every 1 chunk
# (10,000 documents).
lda = \
    gensim.models.ldamodel.LdaModel(
        corpus=mm,
        id2word=id2word,
        num_topics=100,
        update_every=1,
        chunksize=10000,
        passes=1)
# Print the most contributing words for 10 randomly selected topics.
lda.print_topics(10)

# Extract 100 LDA topics, using 20 full passes, no online updates.
lda = \
    gensim.models.ldamodel.LdaModel(
        corpus=mm,
        id2word=id2word,
        num_topics=100,
        update_every=0,
        passes=20)

# A trained model can used be to transform new, unseen documents
# (plain bag-of-words or tf-idf count vectors) into LDA topic
# distributions. Here `doc_bow` would be a set of new documents.
doc_lda = lda[doc_bow]

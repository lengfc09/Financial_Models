# This script illustrates how to use latent semantic analysis (LSA)
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
# Take a look at basic information about the corpus.
print(mm)
# Compute LSA (or LSI as it is sometimes called) of the English
# Wikipedia.
lsi = \
    gensim.models.lsimodel.LsiModel(
        corpus=mm,
        id2word=id2word,
        num_topics=400)
# Print the words that contribute most (both positively and
# negatively) for each of the first ten topics.
lsi.print_topics(10)
# Recover the matrices of the SVD. See
# https://github.com/RaRe-Technologies/gensim/wiki/recipes-&-faq for
# details. Keep in mind that the matrix V is not stored explicitly by
# gensim because it may not fit into memory, as its shape is `num_docs
# * num_topics`. However, you can manually compute it as shown below
# to get it as a 2-dimensional numpy array (i.e. a matrix).
U = lsi.projection.u
Sigma = lsi.projection.s
V = \
    gensim.matutils.corpus2dense(
        corpus=lsi[mm],    # Use gensim's streaming `lsi[corpus]` API.
        num_terms=len(lsi.projection.s)).T / \
    lsi.projection.s

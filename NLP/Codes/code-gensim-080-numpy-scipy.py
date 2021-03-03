# This script illustrates the conversion between numpy/scipy matrices
# and gensim corpora.

import gensim
import numpy as np

# Use a random matrix as an example. This is in fact a dense matrix
# from numpy, which is not as efficient as a sparse matrix (which we
# will discuss further below). The basic idea during the conversion is
# that the numpy matrix has stored the word counts (or whatever vector
# space we're talking about here) such that a text document
# corresponds to a given COLUMN. On the other hand, when you print the
# gensim corpus, each text document corresponds to a given ROW (at
# least when you're printing it in the IPython command shell).
m_np = np.random.randint(10, size=[5, 2])
corpus = gensim.matutils.Dense2Corpus(m_np)
list(corpus)
for doc in corpus:
    print(doc)

# Here we convert the the corpus back into a dense numpy 2D array.
l = max(len(doc) for doc in corpus) # Generator epression.
gensim.matutils.corpus2dense(corpus, num_terms=l)

# Here we use a sparse matrix from SciPy. This can be much more memory
# efficient than a dense matrix, especially when many matrix elements
# are zero (as is often the case in text mining).
import scipy.sparse
m_sp = scipy.sparse.random(5, 2, density=0.5)
m_sp.todense()   # Take a look.
m_sp.A           # Take a look (same as above).
corpus = gensim.matutils.Sparse2Corpus(m_sp)
list(corpus)
for doc in corpus:
    print(doc)

# Convert corpus back to `scipy.sparse.csc` matrix.
gensim.matutils.corpus2csc(corpus)

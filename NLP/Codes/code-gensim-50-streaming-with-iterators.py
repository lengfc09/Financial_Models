# This script shows how you can construct a streaming corpus and then
# pass it on to functionality in gensim. The basic idea is that the
# corpus is not held in memory all at once, but instead processed
# record-by-record. For the purpose of this script, we assume that one
# document corresponds to one file on disk. At the end of the script
# we show an illustration using singular value decomposition.
import gensim, os

def iter_documents(top_directory):
    """This is a generator function: Iterate over all documents, yielding
    one tokenized document (=list of utf8 tokens) at a time. Each
    document corresponds to one file. The generator function finds all
    `.txt` files, no matter how deep under `top_directory`.

    """
    for root, dirs, files in os.walk(top_directory):
        for fname in filter(lambda fname: fname.endswith('.txt'), files):
            # Read each `.txt` document as one big string.
            document = open(os.path.join(root, fname)).read()
            # Break document into utf8 tokens.
            yield gensim.utils.tokenize(document, lower = True, errors = 'ignore')

# Here we print all tokens for all documents. `iter_documents()`
# creates a generator iterator that yields one text document at a
# time. Keep in mind that `gensim.utils.tokenize` itself returns a
# generator iterator for each document, so we have to iterate again
# through `doc_tokens`.
for doc_tokens in iter_documents('.'):
    print('\nNext document:\n')
    for token in doc_tokens:
        print(token)

class TxtSubdirsCorpus(object):
    """This class instantiates an iterable: On each iteration, return
    bag-of-words vectors, one vector for each document. Process one
    document at a time using generators, never load the entire corpus
    into RAM.

    """
    def __init__(self, top_dir): # Constructor method.
        self.top_dir = top_dir   # Save the top-level directory name.
        # Create a dictionary, which is a mapping for documents to
        # sparse vectors.
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
 
    def __iter__(self):         # Define a generator function.
        for doc_tokens in iter_documents(self.top_dir):
            # Transform tokens (strings) into a sparse bag-of-words
            # vector, one document at a time.
            yield self.dictionary.doc2bow(doc_tokens)

# Create the streamed corpus of sparse document vectors. `corpus` is
# an iterable.
corpus = TxtSubdirsCorpus('.')

# Print the corpus vectors. Each vector is sparse and corresponds to
# the contents of one text document.
for vector in corpus:
    print(vector)

# Run truncated Singular Value Decomposition (SVD) on the streamed
# corpus. In this case we give a hint to the SVD algorithm to process
# the input stream in groups of 5000 vectors. This is called
# "chunking" or "mini batching." The return values are as follows: `U`
# contains the left-singular vectors (encoded as a matrix where the
# columns correspond to documents), while `Sigma` contains the
# singular values of the corpus (encoded as a vector).
from gensim.models.lsimodel import stochastic_svd as svd
U, Sigma = \
    svd(
        corpus,
        rank=200,
        num_terms=len(corpus.dictionary),
        chunksize=5000)

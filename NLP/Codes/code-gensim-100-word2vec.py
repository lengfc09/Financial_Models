# This script contains a basic example on how to use word2vec in
# gensim.

# Import modules and set up logging.
import gensim, os, logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

# word2vec expects a sequence of sentences as its input. In this
# example, each sentence is a list of words. This is fine, but
# everything is in RAM so if you have lots of sentences this could be
# a problem. Iterables to the rescue! In fact, all gensim requires is
# to get the sentences sequentially, e.g. using an iterable (see
# further below).
sentences = [['first', 'sentence'], ['second', 'sentence']]
# Train word2vec on the two sentences.
model = gensim.models.Word2Vec(sentences, min_count=1)

# Here we assume the input is on several files on disk, one sentence
# per line. Using an iterable, gensim can process each input file
# line-by-line. It yields one sentence after another.
class MySentences(object):      # This class instantiates an iterable.
    def __init__(self, dirname): # Constructor method.
        self.dirname = dirname
    
    def __iter__(self):         # Here we define a generator function.
        for fname in filter(lambda fname: fname.endswith('.txt'),
                            os.listdir(self.dirname)):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split() # Yield one sentence, split into words.

# Here we get a memory-friendly iterable and hand it over to gensim's
# word2vec. '.' refers to the current directory. Gensim will run
# several passes over the iterable. The first one is to collect words
# and frequencies to build an internal dictionary structure. The later
# ones are to train the neural model.
sentences = MySentences('.')    # Instantiate the class. Create iterable.
model = gensim.models.Word2Vec(sentences)

# If for some reason your input stream is non-repeatable, you can
# perform the steps mentioned above manually. This code is just for
# illustration, it will NOT work in this script as we have not defined
# the 1-pass generators here.
model = gensim.models.Word2Vec(iter=1)  # Empty model, no training yet.
model.build_vocab(some_sentences)  # Can be a non-repeatable, 1-pass generator.
model.train(other_sentences)  # Can be a non-repeatable, 1-pass generator.

# If you want to fine-tune the training, you can change some
# parameters.
model = \
    gensim.models.Word2Vec(
        sentences,
        min_count=10,     # Prune infrequent words. Default is 10.
        size=200,         # Size of neural net layers. Default is 100.
        workers=4)        # Workers for parallelization. Default is 1.

# You can save and load the model to/from file.
model.save('mymodel')
new_model = gensim.models.Word2Vec.load('mymodel')
new_model.train(more_sentences) # You can continue to train it with more sentences.

# Originally, word2vec was released by Google and was written in
# C. You can read from the format used by that implementation as well.
model = Word2Vec.load_word2vec_format('/tmp/vectors.txt', binary=False)
# Using gzipped/bz2 input works too, no need to unzip.
model = Word2Vec.load_word2vec_format('/tmp/vectors.bin.gz', binary=True)

# You can find the most similar words. Here the output might be
# something like "[('queen', 0.50882536)]".
model.most_similar(
    positive=['woman', 'king'],
    negative=['man'],
    topn=1)
# You can check which word does not match. Here the output might be
# 'cereal'.
model.doesnt_match("breakfast cereal dinner lunch";.split())
# You can also check the similarity between different words. Here the
# output might be a number such as 0.74.
model.similarity('woman', 'man')

# If you need the raw output vectors.
model['computer']               # Raw NumPy vector of a word.
# If you want them en-masse as a two-dimensional NumPy matrix.
model.syn()

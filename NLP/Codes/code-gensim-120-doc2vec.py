# This script illustrates doc2vec in gensim. Actually this is more of
# a collection of code snippets, not really a runnable script. In this
# example, we assume that we're interested in sentence-level data (not
# document-level data; in any case, the code would stay very similar
# if you update it to work on whole documents.)

# The input to Doc2Vec is an iterator of `LabeledSentence`
# objects. Each such object represents a single sentence, and consists
# of two simple lists--- list of words and a list of labels. WHY DO WE
# NEED LABELS? Because labels in doc2vec act the same way as words in
# word2vec.
sentence = \
    LabeledSentence(            # Or use `TaggedDocument`.
        words=['some', 'words', 'here'],
        labels=['SENT_1'])

# Here is an example to read text from a file with one sentence per
# line, using the following class as training data. In principle, one
# could have SEVERAL labels per sentence, but the most common
# application is probably to have ONE label per sentence, as shown
# here.
class LabeledLineSentence(object):
    def __init__(self, filename): # Constructor method.
        self.filename = filename
    
    def __iter__(self):         # __iter__() method implemented as generator function.
        for uid, line in enumerate(open(filename)):
            yield LabeledSentence(words=line.split(), labels=['SENT_%s' % uid])

# You can manually control the learning rate as follows, which might
# in some cases yield better results. Or you could randomize the order
# of the input sentences.
model = Doc2Vec(alpha=0.025, min_alpha=0.025) # Use fixed learning rate.
model.build_vocab(sentences)
for epoch in range(10):
    model.train(sentences)
    model.alpha -= 0.002          # Decrease the learning rate.
    model.min_alpha = model.alpha # Fix the learning rate, no decay.

# You can save and load Doc2Vec instances the usual way.
model = Doc2Vec(sentences)
# Store the model to mmap-able files (can map files into memory).
model.save('my_model.doc2vec')
# Load the model back.
model_loaded = Doc2Vec.load('my_model.doc2vec')

# Since labels in doc2vec act in the same way as words in word2vec. So
# to get the most similar words/sentences to the first sentence
# (i.e. label 'SENT_0'), you could type:
print(model.most_similar('SENT_0'))
print(model['SENT_0'])

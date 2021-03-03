# This file shows how to do named entity recognition (NER) using NLTK.
import nltk
sentence = '''In Hong Kong, I like to ride the MTR to visit the HK Space Museum
              and some restaurants rated well by Andy Hayler.'''
to_sentence = nltk.word_tokenize(sentence)
ta_sentence = nltk.pos_tag(to_sentence) # Tag the sentence for parts of speech.
ta_sentence[:3]
# Returns sentence as a tree, with named entities such as PERSON,
# ORGANIZATION, etc.
nltk.ne_chunk(ta_sentence)
# Extract stems of the tree with 'NE' tags, i.e. we're getting all the
# named entities.
ner_sentence = nltk.ne_chunk(ta_sentence, binary=True) # Tags named entities as "NE" only.
for chunk in ner_sentence:
    if hasattr(chunk, 'label') and chunk.label() == 'NE':
        print(chunk)

# If you have more than one sentences, you can adapte the above
# workflow as follows:
article = '''I like riding the MTR. 
             And sometimes I visit the HK Space Museum. 
             Andy Hayler rates restaurants'''
sentences = nltk.sent_tokenize(article)
token_sentences = [nltk.word_tokenize(sent) for sent in sentences]
pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences]
# chunked_sentences = [nltk.ne_chunk(sent, binary=True) for sent in pos_sentences] # Using list compr.
chunked_sentences = nltk.ne_chunk_sents(pos_sentences, binary=True) # Using a generator.
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, 'label') and chunk.label() == 'NE':
            print(chunk)

# We can also plot a pie chart showing how often each named entity
# type appears in the text. For counting we use as usual a
# defaultdict.
from collections import defaultdict
import matplotlib.pyplot as plt
chunked_sentences = nltk.ne_chunk_sents(pos_sentences)
ner_categories = defaultdict(int)
for sent in chunked_sentences:
    for chunk in sent:
        if hasattr(chunk, 'label'):
            ner_categories[chunk.label()] += 1

labels = list(ner_categories.keys())
values = [ner_categories.get(l) for l in labels]
plt.pie(
    values,
    labels=labels,
    autopct='%1.1f%%',          # Add percentages to chart.
    startangle=140)             # Rotate initial start angle.
plt.show()

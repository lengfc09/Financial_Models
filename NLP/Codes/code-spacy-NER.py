# This script shows how to do named entity recognition (NER) with
# spaCy.
import spacy
# Show info about model 'en'. This is a model trained on the English
# language.
spacy.info('en')
# nlp = spacy.load('en')        # Load the 'en' model.
#
# We set all the other options to `False` since we only care about
# `entity` here.
nlp = spacy.load('en', tagger=False, parser=False, matcher=False)
nlp.entity # Entity recognizer object, used to find entities in the text.
doc = \
    nlp(
        'Ottawa is the capital of Canada ' +
        'and the residence of Prime Minister Justin Trudeau.')
doc.ents                        # Document attribute called `ents`.
# Investigate labels for first entity using `label_` attribute.
print(doc.ents[0], doc.ents[0].label_)
print(doc.ents[0].text, doc.ents[0].label_) # Same effect.
# Iterate over `doc.ents` and print out the labels and text.
for ent in doc.ents:
    print(ent.label_, ent.text)

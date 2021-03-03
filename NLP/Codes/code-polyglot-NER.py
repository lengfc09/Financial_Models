# This script shows named entity recognition (NER) with polyglot.
from polyglot.text import Text
text = '''Abraham Lincoln fue un politico y abogado estadounidense 
          que ejercio como decimosexto presidente de los 
          Estados Unidos de America'''
ptext = Text(text) # No need to specify language here; recognized automatically.
ptext.entities # `entities` attribute; see a list of chunks (with label).
for ent in ptext.entities:      # Print each of the entities found.
    print(ent)
type(ent)                    # Print the type of the (last) entity.
ent.tag                      # Tag of (last) entity.
'los' in ent                 # Check is 'los' is in the (last) entity.
'Abraham' in ent             # Is 'Abraham' in the (last) entity?
# List comprehension to get tuples. First tuple element is the entity
# tag, the second is the full string of the entity text (separate by
# space).
[(ent.tag, ' '.join(ent)) for ent in ptext.entities]
# The `pos_tags` attribute queries all the tagged words.
for word, tag in ptext.pos_tags:
    print(word, tag)

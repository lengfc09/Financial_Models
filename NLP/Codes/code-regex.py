# This file contains a few examples of how to use the re module and
# how to deal with regular expressions.
import re                         #  Import 're' module.
re.sub(r'K', r'L', 'King Arthur') #  Replace pattern in string.
re.match(r'abc', 'abcdef')        # Match a substring.
re.search(r'cde', 'abcdef') # Fill also match in the middle of string.
re.match(r'\w+', 'Hello world!') # Match a word.
re.match(r'[a-z0-9 ]+', 'lowercase and nums like 8, but no commas.')
re.split(r'\s+', 'This is a test.') # Returns list split on spaces, e.g. tokenization.
re.findall(r'\w+', "Let's write regex!") # Find all words.
# Split into sentences.
re.split(r'[.?!]', "Hello world! Let's write regex. Isn't this great?")
# Find all capitalized words.
re.findall(r'[A-Z]\w*', 'Hello world, I love Hong Kong.')
re.findall(r'\d+', 'The novel 1984 was published in 1949.')
# Match digits and words (but not anything else, e.g. punctuation).
re.findall('\d+|\w+', 'He has 12 cats.')
m = re.search(r'coconuts', 'I love coconuts.')
print(m.start(), m.end())       # Print start and end indices.
# Find square bracket containing a word (but no space or anything else).
re.search(r'\[\w+\]', 'Hello [wind bla] this is [nice].')

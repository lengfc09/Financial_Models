# This script shows how to download and parse a Wikipedia page using
# Requests and Beautiful Soup. We also use the `re` module for regular
# expressions.
import re
import requests
from bs4 import BeautifulSoup
r = \
    requests.get(
        'https://en.wikipedia.org/wiki/Natural_language_processing',
        timeout=3)
s = BeautifulSoup(r.text, 'lxml')  # Use `lxml` to parse the webpage.
print(s.prettify())               # Take a look at the parsed webpage.
# Extract all the text from the webpage. THIS IS WHAT YOU NEED MOST
# OFTEN FOR NLP AND TEXT ANALYTICS, unless you need to extract only
# part of the webpage.
s.get_text()
# Ways to navigate the data structure.
s.title
s.title.name
s.title.string
s.title.parent.name
s.p               # First 'p' tag.
s.p.get_text()
s.p['class']      # In our example, there's no 'class' HTML attribute.
s.a               # First 'a' tag.
# The difference between the `find` and the `find_all` methods is that
# the former only finds the FIRST child of this tag matching the given
# criterial, while the latter gets ALL of them.
s.find(id='footer')
s.find(style='clear: both;')
# Extract all 'a' tags.
atags = s.find_all('a')           # Find all `<a ...>...</a>` tags.
atags[3]
atags[3].name
atags[3].get('href')  # Get the actual `href` attribute (i.e. the URL).
# If we want to get all `href` attributes, we loop over all `a` tags.
{tag.get('href') for tag in s.find_all('a')}
# Find all tags whose names start with the letter 'b' (in this case
# 'body', 'b', and 'br').
{tag.name for tag in s.find_all(re.compile('^b'))}
# Find all tags whose name contains the letter 't'.
{tag.name for tag in s.find_all(re.compile('t'))}
# We can also pass a list to the `find_all` method, in which case bs4
# allows a string match against any item in that list.
{tag.name for tag in s.find_all(['a', 'body'])}
# Find all the tags in the document, but none of the text
# strings. `True` matches anything it can.
{tag.name for tag in s.find_all(True)}

# how to use selector
[tag.get_text() for tag in s.select(
    "#mw-content-text > div.mw-parser-output > dl:nth-child(56) > dd:nth-child(12)")]

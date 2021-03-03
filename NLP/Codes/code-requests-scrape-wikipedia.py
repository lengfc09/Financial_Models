# This script shows how to use the requests package to scrape a page
# from Wikipedia.
import requests
# Get the response. It is always a good idea to set the `timeout`
# argument in production code. Otherwise your program may hang
# indefinitely.
r = \
    requests.get(
        'https://en.wikipedia.org/wiki/Natural_language_processing',
        timeout=3)
# The following code block is strictly speaking not necessary, but it
# helps you to better understand the response you got.
r.raise_for_status()            # Ensure we notice bad responses.
r.status_code
r.headers['content-type']
r.encoding
print(r.text)                   # `print` gives nicer output for HTML.
r.text.encode('utf-8')          # Use specific encoding.
r.json()            # Doesn't work in this example since no JSON data.
# Finally we write the response content to file.
with open('data-wikipedia-NLP.html', mode='wb') as fd:
    fd.write(r.content)

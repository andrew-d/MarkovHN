#!/usr/bin/env python2

"""
Example usage:
$ ./markov.py data/tptacek.json 100 The NSA
    *** Got 9616 words

    The NSA's hard to be simple opaque session IDs; heavyweight signed cookies
    are a single keypair, and if this confusion is strategic. Pointing this out
    would be be gratuitous, except that Cryptocat's an internal review board
    staffed by federal judges who can issue warrants. This thought also ignores
    the reality that there are in fact, I'm psyched to see discussions about
    things like GTMO distracting themselves from the record which of the
    noisest and most obnoxious people in Congress were elected by mere
    thousands of soldiers in World War II.

"""

from __future__ import print_function

import sys
import json
import warnings

import nltk
import nltk.tokenize


def ununi(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    return s


def main():
    if len(sys.argv) < 3:
        print("Usage: tokenize.py filename.json words_to_generate [start words...]",
              file=sys.stderr)
        return

    js = json.load(open(sys.argv[1], 'rb'))
    words_to_generate = int(sys.argv[2])

    if len(sys.argv) > 3:
        start_words = sys.argv[3:]
    else:
        start_words = None

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')

    words = []
    for comment in js['comments']:
        tokenized = tokenizer.tokenize(ununi(comment))
        words.extend(tokenized)

    print("*** Got %d words" % (len(words,)), file=sys.stderr)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        content_model = nltk.NgramModel(3, words)
        if start_words is None:
            start_words = content_model.generate(100)[-2:]
        content = content_model.generate(words_to_generate, start_words)

    # Trim to period, or add a new one.
    if '.' in content[-5:]:
        trim = -1
        for i in range(len(content) - 5, len(content)):
            if '.' == content[i]:
                trim = i + 1

        if trim != -1:
            print("*** Trimming content at %d..." % (trim,), file=sys.stderr)
            content = content[:trim]
    else:
        content.append('.')

    text = ' '.join(content)

    # Simple punctuation fixes.
    text = text.replace(' ,', ',')
    text = text.replace(' .', '.')
    text = text.replace(' !', '!')
    text = text.replace(' ?', '?')
    text = text.replace('( ', '(')
    text = text.replace(' )', ')')
    text = text.replace(' ;', ';')
    text = text.replace(" ' ", "'")

    # Done!
    print(text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

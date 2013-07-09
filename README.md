# The HN Markov Generator

Inspired by [this tweet](https://twitter.com/tqbf/status/354653565169569792), I created a simple Markov generator and a scraper for a user's HN comments.  Deliberately left out so I don't get yelled at: the bot that posts these comments to HN.

Comment data from tptacek is included :-)

# Usage

    python extract.py username > username.json
    python markov.py username.json 100 Starting word

You need Python and some requirements installed.  Do this:

    virtualenv markov
    . ./markov/bin/activate
    pip install -r requirements.txt

# License

[WTFPL](http://en.wikipedia.org/wiki/WTFPL)

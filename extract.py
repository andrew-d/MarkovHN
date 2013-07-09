#!/usr/bin/env python2

"""
Extract the given number of comments from a user's HN history.
Prints them to stdout as a JSON object with format:
    {"comments" : ["array", "of", "comments"]}
"""

from __future__ import print_function

import sys
import json
import time
import requests
from bs4 import BeautifulSoup


def extract_comments(page, username):
    comments = page.find_all('a', href='user?id=%s' % (username,))

    ret = []
    for comment in comments:
        # td > div > span > a, so reverse
        toplevel = comment.parent.parent.parent
        text_elem = toplevel.find('span', class_='comment')
        ret.append(text_elem.text)

    return ret


def main():
    if len(sys.argv) < 2:
        print("Usage: extract.py <username> [limit]", file=sys.stderr)
        return

    if len(sys.argv) >= 3:
        limit = int(sys.argv[2])
    else:
        limit = 100

    username = sys.argv[1]
    url = 'https://news.ycombinator.com/threads?id=%s' % (username,)
    page_num = 0
    has_next = False
    final = []

    while len(final) < limit:
        page_num += 1
        print("*** Fetching comments page #%d..." % (page_num,), file=sys.stderr)

        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            print("*** Error requesting page: %s" % (e,), file=sys.stderr)
            return

        if not r.ok:
            print("*** Error getting page: %d %s" % (r.status, r.reason), file=sys.stderr)
            return

        print("*** Extracting comments...", file=sys.stderr)
        page = BeautifulSoup(r.content)
        comments = extract_comments(page, username)
        final.extend(comments)
        print("*** Have %d comments so far, %d from this page" % (len(final), len(comments)),
              file=sys.stderr)

        # Find the "next" link.
        has_next = False
        next = page.find('td', class_='title')
        if next is not None:
            next_link = next.find('a')

            if next_link is not None:
                url = next_link.attrs['href']
                if url.startswith('/'):
                    url = 'https://news.ycombinator.com' + url

                has_next = True

        if not has_next:
            break

        print("*** Rate-limiting...", file=sys.stderr)
        time.sleep(1)

    print(json.dumps({"comments": final}))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

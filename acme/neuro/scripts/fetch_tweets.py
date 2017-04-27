import argparse

import acme.neuro.scripts.helpers as _helpers
_helpers.setup_logging()

import acme.tools.twitter_api as _twitter_api


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang')
    parser.add_argument('--search')
    args = parser.parse_args()

    data = _twitter_api.fetch_tweets(
        lang=args.lang,
        search=args.search,
    )

    for d in data:
        print d

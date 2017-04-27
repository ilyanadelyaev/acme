# coding: utf8
from __future__ import unicode_literals

import logging

import TwitterSearch

import acme.exc as exc

from acme.tools.config import config


logger = logging.getLogger(__name__)


class TwitterError(exc.AcmeError):
    pass


def fetch_tweets(
        lang,
        search,
):
    search = search.encode('utf8')

    logger.debug(
        'Search for (%s) tweets: %s',
        lang, search,
    )

    data = []

    try:
        twitter_search = TwitterSearch.TwitterSearch(
            consumer_key=config['twitter/consumer_key'],
            consumer_secret=config['twitter/consumer_secret'],
            access_token=config['twitter/access_token'],
            access_token_secret=config['twitter/access_token_secret'],
        )

        tso = TwitterSearch.TwitterSearchOrder()
        tso.set_keywords(search.split())
        tso.set_language(lang)
        tso.set_include_entities(False)

        for tweet in twitter_search.search_tweets_iterable(tso):
            data.append({
                'author': tweet['user']['screen_name'],
                'text': tweet['text'],
            })

    except TwitterSearch.TwitterSearchException as ex:
        err = '({}) {}'.format(
            ex.__class__.__name__,
            str(ex),
        )
        logger.error(err)
        raise TwitterError(err)

    return data

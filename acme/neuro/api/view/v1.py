# coding: utf8
from __future__ import unicode_literals

import logging

import flask

import acme.tools.twitter_api as _twitter_api

from acme.lib.rest import base as rest_base

import acme.neuro.logic.rnn as _rnn


logger = logging.getLogger(__name__)


def register(app):
    """
    Views register
    """
    blueprint = flask.Blueprint('v1', __name__, url_prefix='/api/v1/')
    #
    View(blueprint)
    #
    app.flask_app.register_blueprint(blueprint)


class View(rest_base.JSONView):
    ROUTE_ROOT = '{}/'

    def __init__(self, blueprint):
        self.ping__get(blueprint)
        self.tweets__get(blueprint)

    def ping__get(self, blueprint):
        def processor():
            try:
                # pylint: disable=E1101
                import acme.neuro.api.version
                version = acme.neuro.api.version.VERSION
            except ImportError:
                version = '0'
            #
            return {
                'version': version,
            }

        self._route(
            blueprint,
            'ping', 'GET',
            processor,
        )

    def tweets__get(self, blueprint):
        parser = self._request_parser()
        parser.add_argument(
            'search',
            location='args',
            default='',
        )
        parser.add_argument(
            'lang',
            location='args',
            default='ru',
        )

        def processor():
            args = parser.parse_args()
            #
            objects = _twitter_api.fetch_tweets(
                lang=args.lang,
                search=args.search,
            )
            #
            sentences = []
            for o in objects:
                sentences.append(o['text'])
            result = _rnn.predict(
                self._g.model,
                self._g.model_dictionary,
                sentences,
            )
            values = []
            for i, o in enumerate(objects):
                o['value'] = int(result[i][0] * 100.0)
                values.append(o['value'])
            #
            return {
                'objects': objects,
                'count': len(objects),
                'average_value': (sum(values) / float(len(values))),
            }

        self._route(
            blueprint,
            'tweets', 'GET',
            processor,
        )

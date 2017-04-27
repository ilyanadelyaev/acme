# coding: utf8
from __future__ import unicode_literals

import logging

import flask

from acme.lib.rest import base as rest_base


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

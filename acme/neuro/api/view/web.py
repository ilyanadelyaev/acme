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
    blueprint = flask.Blueprint('web', __name__, url_prefix='/')
    #
    View(blueprint)
    #
    app.flask_app.register_blueprint(blueprint)


class View(rest_base.BaseView):
    ROUTE_ROOT = '{}/'

    def __init__(self, blueprint):
        self.index__get(blueprint)

    def index__get(self, blueprint):
        def processor():
            return flask.render_template(
                'index.html',
            )

        self._route(
            blueprint,
            '', 'GET',
            processor,
        )

import logging

import flask

from acme.tools import logger_setup

from acme.tools.config import config

import acme.neuro.api.view.registry as view_registry


logger = logging.getLogger(__name__)


class Application(object):
    def __init__(self):
        # flask app
        self.flask_app = flask.Flask('acme.neuro.api')

        # register flask
        view_registry.register_flask_callbacks(self)
        view_registry.register_views(self)

        # logging
        handler = logger_setup.setup_logging(
            level=config['neuro/api/logger/level'],
            handler_type=config['neuro/api/logger/handler_type'],
            path=config['neuro/api/logger/path'],
            filename=config['neuro/api/logger/filename'],
        )

        # flask logger
        self.flask_app.logger.addHandler(handler)
        self.flask_app.logger.setLevel(config['neuro/api/logger/level'])

        logger.info('Initialized')

import logging

import flask

from acme.tools import logger_setup

from acme.tools.config import config

import acme.neuro.api.view.registry as view_registry

import acme.neuro.logic.rnn as _rnn
import acme.neuro.logic.corpus as _corpus


logger = logging.getLogger(__name__)


class Application(object):
    def __init__(self):
        # neuro model
        self.model = _rnn.load_model()
        self.model_dictionary = _corpus.load_dictionary()

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

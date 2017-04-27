import uuid
import logging
import copy
import json

import flask


logger = logging.getLogger(__name__)


def register_views(app):
    """
    Views register magic
    """
    import acme.neuro.api.view.web as web
    import acme.neuro.api.view.v1 as v1
    #
    for module in (web, v1, ):
        module.register(app)


def register_flask_callbacks(application):
    """
    Register here all specific methods per-request call
    """

    # callback functiion
    # pylint: disable=W0612
    @application.flask_app.before_request
    def before_request():
        """
        - Set request_id
        - Log request data
        """
        # request id
        flask.g.request_id = str(uuid.uuid4())
        # logging
        request = flask.request
        message = '[{}] {} -> ({} {}) "{}"'.format(
            flask.g.request_id,
            request.remote_addr,
            request.path, request.method,
            dict(flask.request.args),
        )
        if request.mimetype == 'application/json':
            data = copy.deepcopy(request.json)
            message += ' {}'.format(data)
        logger.debug(message)
        # sentry
        if hasattr(application, 'sentry'):
            flask.g.sentry = application.sentry

    # callback functiion
    # pylint: disable=W0612
    @application.flask_app.after_request
    def after_request(resp):
        """
        - Log request data
        """
        message = '[{}] ({})'.format(
            flask.g.request_id,
            resp.status_code,
        )
        if resp.mimetype == 'application/json':
            message += ' {}'.format(resp.data.replace('\n', ''))
        logger.debug(message)
        return resp

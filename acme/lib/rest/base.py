import abc
import logging

import flask

import acme.lib.rest.reqparse as reqparse

import acme.exc as exc

import acme.permissions


logger = logging.getLogger(__name__)


class Permissions(object):
    __metaclass__ = abc.ABCMeta

    __PERMISSIONS_NAMES = acme.permissions.names(
        acme.permissions.PERMISSIONS
    )

    PERMISSIONS_ROOT = '{}'

    def _permission_value(self, permission_name):
        permission_name = self.PERMISSIONS_ROOT.format(permission_name)
        return self.__PERMISSIONS_NAMES.get(permission_name)

    def check_permission(self, permission_name):
        user_name = flask.g.extra['user']['name']
        #
        permission_name = self.PERMISSIONS_ROOT.format(permission_name)
        #
        permission_value = self.__PERMISSIONS_NAMES.get(permission_name)
        if permission_value is None:
            raise exc.PermissonDenied(
                user_name,
                'INVALID PERMISSION: {}'.format(permission_name),
            )
        #
        user_permissions = flask.g.extra['user']['permissions']
        #
        system_permissions = user_permissions.get('system', set())
        super_permissions = self._super_permissions(user_permissions)
        permissions = system_permissions | super_permissions
        #
        if permission_value not in permissions:
            raise exc.PermissonDenied(
                user_name,
                permission_name,
                permission_value,
            )

    def _super_permissions(self, user_permissions):
        return set()


class BaseView(Permissions):
    __metaclass__ = abc.ABCMeta

    ROUTE_ROOT = None

    @property
    def _g(self):
        return flask.g

    def _request_parser(self):
        return reqparse.RequestParser()

    @staticmethod
    def _parse_sort_aggr(raw_sort_data):
        sort_params = {}
        for param in raw_sort_data.split(','):
            if param.startswith('-'):
                sort_params[param[1:]] = -1
            else:
                sort_params[param] = 1
        return sort_params

    @staticmethod
    def _parse_sort(raw_sort_data):
        sort_params = list()
        for param in raw_sort_data.split(','):
            if param.startswith('-'):
                sort_params.append((param[1:], -1))  # DESCENDING
            else:
                sort_params.append((param, 1))  # ASCENDING
        return sort_params

    def _list_request_parser(self):
        parser = self._request_parser()
        parser.add_argument(
            'skip',
            location='args',
            required=False,
            type=int,
        )
        parser.add_argument(
            'limit',
            location='args',
            required=False,
            type=int,
        )
        parser.add_argument(
            'sort',
            location='args',
            required=False,
            type=self._parse_sort
        )
        return parser

    def _route(self, blueprint, route, method, func):
        route = self.ROUTE_ROOT.format(route)
        route = route.replace('//', '/')
        #
        endpoint = route.replace('<', '').replace('>', '')
        endpoint = endpoint.strip('/').replace('/', '__')
        endpoint = '__'.join((blueprint.name, endpoint, method.lower()))
        #
        blueprint.route(
            route,
            methods=[method],
            endpoint=endpoint,
        )(self._processor(func))

    def _processor(self, func):
        def wrapper(**kw):
            return func()
        return wrapper


class JSONView(BaseView):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def json_body():
        return flask.request.json

    @staticmethod
    def raw_form():
        return flask.request.form

    @staticmethod
    def raw_files():
        return flask.request.files

    @staticmethod
    def raw_args():
        return flask.request.args

    @staticmethod
    def _func(func):
        return flask.jsonify(
            func()
        ), 200

    def _processor(self, func):
        def wrapper(**kw):
            try:
                return self._func(func)
            except (
                    exc.AcmeError,
            ) as ex:
                logger.exception('_processor error')
                return flask.jsonify(ex.json()), ex.status_code
            #
            except Exception as ex:  # pylint: disable=W0703
                logger.exception('_processor error')
                error_message = 'Internal error: {}'.format(ex.message)
                return flask.jsonify({
                    'error': error_message,
                }), 500
        #
        return wrapper

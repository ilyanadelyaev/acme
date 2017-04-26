class AcmeError(Exception):
    status_code = 400

    def json(self):
        return {
            'error': self.message,
        }


class PermissonDenied(AcmeError):
    status_code = 401

    def __init__(
            self,
            user,
            permission_name,
            permission_id=None,
    ):
        err = u'Permission denied for "{}" with: {} [{}]'.format(
            user,
            permission_name,
            permission_id,
        )
        super(PermissonDenied, self).__init__(err)
        #
        self.permission_name = permission_name
        self.permission_id = permission_id

    def json(self):
        return {
            'error': self.message,
            'permission_name': self.permission_name,
            'permission_id': self.permission_id,
        }


class InvalidArgument(AcmeError):
    def __init__(self, arg, val):
        super(InvalidArgument, self).__init__(
            u'Invalid argument "{}": "{}"'.format(
                arg, val if val else ':empty:'))

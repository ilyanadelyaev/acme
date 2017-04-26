PERMISSIONS = {
    'NEURO': {
        'API': {
            'V1': {
            },
        },
    },
}


def __collect(root, key=None):
    result = {}
    for k, v in root.iteritems():
        if v is None:
            continue
        kk = ':'.join((key, k)) if key else k
        if isinstance(v, dict):
            result.update(__collect(v, key=kk))
        else:
            result[kk] = v
    return result


def names(root, key=None):
    return __collect(root, key)


def values(root, key=None):
    permissions = __collect(root, key=key)
    return dict(((v, k) for (k, v) in permissions.iteritems()))

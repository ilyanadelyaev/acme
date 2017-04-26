import acme.permissions as p


class TestLogicPermissions:
    def test__permissions__unique(self):
        permissions = p.names(p.PERMISSIONS)
        #
        __keys = list((k for (k, v) in permissions.iteritems()))
        if len(__keys) != len(set(__keys)):
            __items = set()
            __invalid = list()
            for k in __keys:
                if k not in __items:
                    __items.add(k)
                else:
                    __invalid.append(k)
            assert not __invalid
        #
        __values = list((v for (k, v) in permissions.iteritems()))
        if len(__values) != len(set(__values)):
            __items = set()
            __invalid = list()
            for k in __values:
                if k not in __items:
                    __items.add(k)
                else:
                    __invalid.append(k)
            assert not __invalid

    def test__permissions_values__unique(self):
        permissions_values = p.values(p.PERMISSIONS)
        #
        __keys = list((k for (k, v) in permissions_values.iteritems()))
        if len(__keys) != len(set(__keys)):
            __items = set()
            __invalid = list()
            for k in __keys:
                if k not in __items:
                    __items.add(k)
                else:
                    __invalid.append(k)
            assert not __invalid
        #
        __values = list((v for (k, v) in permissions_values.iteritems()))
        if len(__values) != len(set(__values)):
            __items = set()
            __invalid = list()
            for k in __values:
                if k not in __items:
                    __items.add(k)
                else:
                    __invalid.append(k)
            assert not __invalid

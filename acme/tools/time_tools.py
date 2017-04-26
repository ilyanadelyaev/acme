__INTERVALS = [1, 60, 3600, 86400, 604800, 2419200, 29030400]
__NAMES = [
    ('sec', 'sec'),
    ('min', 'min'),
    ('hour', 'hours'),
    ('day', 'days'),
    ('week', 'weeks'),
    ('month', 'months'),
    ('year', 'years'),
]


def sec_to_str(seconds):
    if seconds is None:
        return
    #
    amount = int(seconds)
    result = []
    for i in xrange(len(__NAMES) - 1, -1, -1):
        a = amount / __INTERVALS[i]
        if a > 0:
            result.append((a, __NAMES[i][1 % a]))
            amount -= a * __INTERVALS[i]
    # cut tail
    result = result[:2]
    #
    return ' '.join(('{} {}'.format(a, n) for a, n in result))

from os.path import dirname, abspath, join
from collections import deque

PATH = dirname(abspath(dirname(__file__)))

NAMESPACES = {
    'LOGGING': {
        'CFG': join(PATH, 'Config', 'logging.conf'),
    },
    'BACKEND': {
        'CFG': join(PATH, 'Config', 'dbconn.conf'),
    },
    'IPLOCATE': {
        'DB': join(PATH, 'BasicData', 'ip_to_country.db')
    }
}


def flatten(d, ns=''):
    stack = deque([(ns, d)])
    while stack:
        name, space = stack.popleft()
        for key, value in space.items():
            if isinstance(value, dict):
                stack.append((name + key + '_', value))
            else:
                yield name + key, value

DEFAULTS = dict((key, value) for key, value in flatten(NAMESPACES))

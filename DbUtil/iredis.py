#!/usr/bin/env python
# coding=utf-8
import logging
try:
    import redis
except ImportError:
    redis = None


def get_redis_conn(**kwargs):
    cfg = {}
    cfg['host'] = kwargs['host']
    cfg['port'] = int(kwargs['port'])
    cfg['password'] = kwargs.get('password', None)
    cfg['db'] = kwargs.get('db', 0)
    conn = redis.Redis(**cfg)
    logging.info('REDIS - CONNECTION %s - SUCCEED' % conn)
    return conn

if __name__ == '__main__':
    print get_redis_conn(**{'host': '10.59.105.77', 'port': 27017})

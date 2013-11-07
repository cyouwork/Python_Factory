#!/usr/bin/env python
# coding=utf-8
import logging
try:
    import pymongo
except ImportError:
    pymongo = None

version = "0.1"
version_info = (0, 1, 0, 0)


def get_mongo_conn(**kwargs):
    cfg = {}
    cfg['port'] = int(kwargs['port'])
    cfg['host'] = kwargs['host']
    cfg['auto_start_request'] = False
    conn = pymongo.Connection(**cfg)
    logging.info(conn)
    return conn

if __name__ == '__main__':
    print get_mongo_conn(**{'host': '10.59.105.77', 'port': 27017})

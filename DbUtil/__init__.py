#!/opt/17173/logv3/bin/python2.7
# coding=utf-8
# author=season


import os
from itorndb import Connection as MysqlConnection
from cxoradb import Connection as OracleConnection
from mongodb import get_mongo_conn
from iredis import get_redis_conn
from Common.configParser import ConfigParser
from Config.defaults import DEFAULTS


class ConnTypeNotFound(Exception):
    pass


class DbConn(object):

    '''数据库连接返回'''

    def __init__(self, conf=DEFAULTS['BACKEND_CFG']):
        self.config = ConfigParser()
        self.config.read(conf)

    def get_conn(self, cid):
        return self.create_conn(cid)

    def create_conn(self, cid):
        config = dict(self.config.items(cid))
        cid_splits = cid.upper().split('_')
        if 'MYSQL' in cid_splits:
            return MysqlConnection(**config)
        elif 'ORACLE' in cid_splits:
            return OracleConnection(**config)
        elif 'MONGO' in cid_splits:
            return get_mongo_conn(**config)
        elif 'REDIS' in cid_splits:
            return get_redis_conn(**config)
        else:
            raise ConnTypeNotFound('数据库连接类型未定义: %s' % cid)

if __name__ == '__main__':
    DbConn().get_conn('')

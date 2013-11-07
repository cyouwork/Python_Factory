#!/opt/17173/logv3/bin/python2.7
# coding=utf-8
# author=season
import os
import cx_Oracle
try:
    import pymongo
except ImportError:
    pymongo = None
import redis
import logging
from mysql import connector
from configParser import ConfigParser
from cx_Oracle import InterfaceError
from Config.defaults import DEFAULTS


'''数据库操作模块'''


class Singleton(type):

    _instance = {}

    def __init__(cls, name, bases, dct):
        super(Singleton, cls).__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class DbConn(object):

    __metaclass__ = Singleton

    def __init__(self, conf=DEFAULTS['BACKEND_CFG']):
        '''初始化日志模块、配置信息'''

        self.config = ConfigParser()
        self.config.read(conf)
        self.dbconn_dict = {}

    def oracle_conn_test(self, oracle_conn):
        if oracle_conn:
            try:
                oracle_conn.ping()
            except InterfaceError, err:
                logging.warn(err.__class__.__name__ + ':' + str(err))
                oracle_conn = None
        return oracle_conn

    def __del__(self):
        '''在该类的实例被销毁时断开数据库连接'''

        for cid, dbconn in self.dbconn_dict.items():
            if dbconn:
                try:
                    dbconn.close()
                    logging.info('DATABASE - CONNECTION - %s - %s - CLOSED' % (cid, dbconn))
                except Exception, err:
                    logging.warn(err.__class__.__name__ + ':' + str(err))
        self.dbconn_dict = {}

    def get_mongouri_conn(self, cid='37WW_MONGO'):
        mongo_conn = self.dbconn_dict.setdefault(cid, None)
        if not mongo_conn:
            mongo_uri = 'mongodb://{user}:{passwd}@{host}:{port}/{database}'.format(**dict(self.config.items(cid)))
            mongo_conn = pymongo.Connection(mongo_uri)
            self.dbconn_dict[cid] = mongo_conn
        return mongo_conn

    def get_mongo_conn(self, cid='37WW_MONGO'):
        mongo_conn = self.dbconn_dict.setdefault(cid, None)
        if not mongo_conn:
            cfg, cfg_extra = dict(self.config.items(cid)), {}
            cfg_extra['host'] = cfg['host']
            cfg_extra['port'] = int(cfg['port'])
            mongo_conn = pymongo.Connection(**cfg_extra)
            self.dbconn_dict[cid] = mongo_conn
            logging.info('MONGODB - CONNECTION %s - SUCCEED' % mongo_conn)
        return mongo_conn

    def get_redis_conn(self, cid='EXCHANGE_REDIS'):
        redis_conn = self.dbconn_dict.setdefault(cid, None)
        if not redis_conn:
            cfg = dict(self.config.items(cid))
            cfg['port'] = int(cfg['port'])
            redis_conn = redis.Redis(**cfg)
            self.dbconn_dict[cid] = redis_conn
            logging.info('REDIS - CONNECTION %s - SUCCEED' % redis_conn)
        return redis_conn

    def get_oracle_conn(self, cid='CX_ORACLE', ci_flag=False):

        tns = '{user}/{password}@{host}:{port}/{database}'.format(**dict(self.config.items(cid)))

        oracle_conn = self.dbconn_dict.setdefault(cid, None)
        oracle_conn = self.oracle_conn_test(oracle_conn)
        if not oracle_conn:
            try:
                oracle_conn = cx_Oracle.connect(tns)
            except Exception, err:
                logging.error(err)
                raise err  # 连接异常时直接抛出错误
            else:
                oracle_conn.autocommit = ci_flag  # 提交标志
                self.dbconn_dict[cid] = oracle_conn
                logging.info('ORACLE - CONNECTION %s - SUCCEED' % oracle_conn)
        return oracle_conn

    def get_mysql_conn(self, cid='WW_MYSQL'):
        mysql_conn = self.dbconn_dict.setdefault(cid, None)
        if not mysql_conn:
            try:
                cfg = dict(self.config.items(cid))
                cfg['port'] = int(cfg['port'])
                mysql_conn = connector.connect(**cfg)
            except Exception, err:
                logging.error(err)
                raise err  # 连接异常时直接抛出错误
            else:
                self.dbconn_dict[cid] = mysql_conn
                logging.info('MYSQL - CONNECTION %s - SUCCEED' % mysql_conn)
        return mysql_conn


if __name__ == '__main__':
    dbconn = DbConn()

#!/usr/bin/env python
# coding=utf-8

"""围绕mysql官方python数据库驱动，对torndb极简改造
torndb原为facebook/tornado的一部分，自3.0版本后已经剥离成独立的开源项目"""

from __future__ import absolute_import, division, with_statement

import copy
import itertools
import logging
import os
import time

try:
    from mysql import connector
except ImportError:
    connector = None

version = "0.1"
version_info = (0, 1, 0, 0)


class Connection(object):

    """mysql连接轻量级工具"""

    def __init__(self, **kwargs):
        self.host = kwargs.get('host', '127.0.0.1')
        self.database = kwargs.get('database', 'test')
        self.port = int(kwargs.get('port', 3306))
        self._user = kwargs.get('user', None)
        self._passwd = kwargs.get(
            'password', kwargs.get('passwd', None))
        self.max_idle_time = float(kwargs.get('max_idle_time', 7 * 3600))
        self._db = None
        self._db_args = {
            'use_unicode': True,
            'charset': "utf8",
            'sql_mode': "TRADITIONAL",
            'host': self.host,
            'database': self.database,
            'port': self.port,
            'user': self._user,
            'passwd': self._passwd
        }
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.host,
                          exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """关闭数据库连接"""
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def commit(self):
        """数据库操作提交"""
        if getattr(self, "_db", None) is not None:
            self._db.commit()

    def rollback(self):
        """数据库操作回滚"""
        if getattr(self, "_db", None) is not None:
            self._db.rollback()

    def reconnect(self):
        """关闭现有的数据库连接并重连"""
        self.close()
        self._db = connector.Connect(**self._db_args)
        self._db.autocommit = False

    def iter(self, query, *args, **kwargs):
        """以迭代器的方式返回查询结果"""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            column_names = [d[0] for d in cursor.description]
            for row in cursor:
                yield Row(zip(column_names, row))
        finally:
            cursor.close()

    def query(self, query, *args, **kwargs):
        """以列表方式返回查询结果"""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *args, **kwargs):
        """返回唯一的查询结果"""
        rows = self.query(query, *args, **kwargs)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def execute(self, query, *args, **kwargs):
        """执行给定的query并返回影响的最后一条记录的主键id"""
        return self.execute_lastrowid(query, *args, **kwargs)

    def execute_lastrowid(self, query, *args, **kwargs):
        """执行给定的query并返回影响的最后一条记录的主键id"""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *args, **kwargs):
        """执行给定的query并返回影响记录条数"""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, args):
        """多条执行，返回影响的最后一条记录的主键id"""
        return self.executemany_lastrowid(query, args)

    def executemany_lastrowid(self, query, args):
        """多条执行，返回影响的最后一条记录的主键id"""
        cursor = self._cursor()
        try:
            cursor.executemany(query, args)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, args):
        """多条执行，返回影响记录条数"""
        cursor = self._cursor()
        try:
            cursor.executemany(query, args)
            return cursor.rowcount
        finally:
            cursor.close()

    update = execute_rowcount
    updatemany = executemany_rowcount

    insert = execute_lastrowid
    insertmany = executemany_lastrowid

    def _ensure_connected(self):
        '''确认数据库处于连接状态，否则重连'''
        if (self._db is None or (not self._db.is_connected()) or 
                (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, args, kwargs):
        try:
            return cursor.execute(query, kwargs or args)
        except connector.errors.OperationalError:
            logging.error("Error connecting to MySQL on %s", self.host)
            self.close()
            raise


class Row(dict):

    """继承自字典类型，使其能进行属性引用"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if __name__ == '__main__':
    pass

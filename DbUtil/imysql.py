
# coding=utf-8
import logging
from configParser import ConfigParser
from mysql import connector
from Config.defaults import DEFAULTS


DB_CONFIG = ConfigParser()
DB_CONFIG.read(DEFAULTS['BACKEND_CFG'])
dbconfig = DB_CONFIG.items('KVM_MYSQL_TEST')

def get_mysql_conn(cid='KVM_MYSQL_TEST'):
    #mysql_conn = self.dbconn_dict.setdefault(cid, None)
    cfg = dict(DB_CONFIG.items(cid))
    cfg['port'] = int(cfg['port'])
    mysql_conn = connector.connect(**cfg)

    return mysql_conn
    
#    if not mysql_conn:
#        try:
#            cfg = dict(self.config.items(cid))
#            cfg['port'] = int(cfg['port'])
#            mysql_conn = connector.connect(**cfg)
#        except Exception, err:
#            logging.error(err)
#            raise err  # 连接异常时直接抛出错误
#        else:
#            self.dbconn_dict[cid] = mysql_conn
#            logging.info('MYSQL - CONNECTION %s - SUCCEED' % mysql_conn)
#    return mysql_conn


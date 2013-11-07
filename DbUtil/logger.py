# -*- coding: UTF-8 -*-
from os.path import dirname, abspath
import logging
from logging import config
from Config.defaults import DEFAULTS


def getlogger(conf=DEFAULTS['LOGGING_CFG'], log='common'):
    logging.config.fileConfig(conf)
    logger = logging.getLogger(log)
    return logger

if __name__ == '__main__':
    logger = getlogger()
    logger.debug('test message.')

#!/usr/bin/env python
# coding=utf-8
import sys
import os
import socket
import logging
import logging.handlers
from toughlib import dispatch
from twisted.logger import Logger
import functools

EVENT_INFO = 'syslog_info'
EVENT_DEBUG = 'syslog_debug'
EVENT_ERROR = 'syslog_error'
EVENT_EXCEPTION = 'syslog_exception'
EVENT_SETUP = 'syslog_setup'

__default_logger_ = Logger()

def string_to_level(log_level):
    if log_level == "CRITICAL":
        return logging.CRITICAL
    if log_level == "ERROR":
        return logging.ERROR
    if log_level == "WARNING":
        return logging.WARNING
    if log_level == "INFO":
        return logging.INFO
    if log_level == "DEBUG":
        return logging.DEBUG
    return logging.NOTSET


class Logger:

    def __init__(self,config):
        self.setup(config)

    def setup(self, config):
        self.syslog_enable = config.syslog.enable
        self.syslog_server = config.syslog.server
        self.syslog_port = config.syslog.port
        self.syslog_level = config.syslog.level
        self.syslog_shost = config.syslog.shost
        self.formatter = logging.Formatter(
            u'%(asctime)s {0} %(name)s %(levelname)-8s %(module)s -> %(funcName)s (%(lineno)d) %(message)s'.format(self.syslog_shost),
            '%b %d %H:%M:%S', )
        self.level = string_to_level(self.syslog_level)
        if config.system.debug:
            self.level = string_to_level("DEBUG")

        self.syslogger = logging.getLogger('toughstruct')
        self.syslogger.setLevel(self.level)

        if self.syslog_enable and self.syslog_server:
            handler = logging.handlers.SysLogHandler(address=(self.syslog_server, self.syslog_port))
            handler.setFormatter(self.formatter)
            self.syslogger.addHandler(handler)


        self.info = self.syslogger.info
        self.debug = self.syslogger.debug
        self.warning = self.syslogger.warning
        self.error = self.syslogger.error
        self.critical = self.syslogger.critical
        self.log = self.syslogger.log
        self.msg = self.syslogger.info
        self.err = self.syslogger.error

    def event_syslog_setup(self,config):
        self.setup(config)

    def event_syslog_info(self, msg):
        self.info(msg)

    def event_syslog_debug(self, msg):
        self.debug(msg)

    def event_syslog_error(self, msg):
        self.error(msg)

    def event_syslog_exception(self, err):
        self.syslogger.exception(err)


setup = functools.partial(dispatch.pub, EVENT_SETUP) 



def info(message,**kwargs):
    if EVENT_INFO in dispatch.callbacks:
        dispatch.pub(EVENT_INFO,message,**kwargs)
    else:
        __default_logger_.info(message)


def debug(message,**kwargs):
    if EVENT_DEBUG in dispatch.callbacks:
        dispatch.pub(EVENT_DEBUG,message,**kwargs)
    else:
        __default_logger_.debug(message)


def error(message,**kwargs):
    if EVENT_ERROR in dispatch.callbacks:
        dispatch.pub(EVENT_ERROR,message,**kwargs)
    else:
        __default_logger_.error(message)


exception = functools.partial(dispatch.pub, EVENT_EXCEPTION)


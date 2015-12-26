#!/usr/bin/env python
# coding=utf-8
import sys
import socket
import logging
import logging.handlers



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
        self.config = config
        self.formatter = logging.Formatter(
            u'%(asctime)s {0} %(name)s %(levelname)-8s %(module)s -> %(funcName)s (%(lineno)d) %(message)s'.format(config.syslog.shost),
            '%b %d %H:%M:%S', )
        self.syslog_enable = config.syslog.enable
        self.syslog_server = config.syslog.server
        self.syslog_port = config.syslog.port
        if self.syslog_server:
            self.syslog_address = (self.config.syslog.server,self.config.syslog.port`)
        self.level = string_to_level(config.syslog.get('level', 'INFO'))
        if config.default.debug:
            self.level = string_to_level("DEBUG")

        self.syslogger = logging.getLogger('toughstruct')
        self.syslogger.setLevel(self.level)

        if self.syslog_enable and self.syslog_server:
            handler = logging.handlers.SysLogHandler(address=(self.syslog_server, self.syslog_port))
            handler.setFormatter(self.formatter)
            self.syslogger.addHandler(handler)

        if self.config.default.debug:
            stream_handler = logging.StreamHandler(sys.stderr)
            stream_handler.setFormatter(self.formatter)
            self.syslogger.addHandler(stream_handler)

        self.info = self.syslogger.info
        self.debug = self.syslogger.debug
        self.warning = self.syslogger.warning
        self.error = self.syslogger.error
        self.critical = self.syslogger.critical
        self.log = self.syslogger.log
        self.msg = self.syslogger.info
        self.err = self.syslogger.error


#!/usr/bin/env python
#coding=utf-8

import treq
from twisted.internet import reactor
from twisted.internet import defer
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from twisted.web.client import HTTPConnectionPool

pool = HTTPConnectionPool(reactor)

class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


def get(url,**kwargs):
    return treq.get(url, pool=pool,data_to_body_producer=StringProducer,**kwargs)

def post(url,data=None,**kwargs):
    return treq.post(url, data=data, pool=pool,data_to_body_producer=StringProducer,**kwargs)





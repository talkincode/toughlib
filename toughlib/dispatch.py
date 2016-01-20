#!/usr/bin/env python
# coding=utf-8

import types
from twisted.internet.threads import deferToThread
from twisted.python import reflect
from twisted.internet import defer

class EventDispatcher:

    def __init__(self, prefix="event_"):
        self.prefix = prefix
        self.callbacks = {}


    def sub(self, name, func):
        self.callbacks.setdefault(name, []).append(func)


    def register(self, obj):
        d = {}
        reflect.accumulateMethods(obj, d, self.prefix)
        for k,v in d.items():
            self.sub(k, v)

    def pub(self, name, *args, **kwargs):
        if name not in self.callbacks:
            return
        async = kwargs.pop("async",False)
        results = []
        for func in self.callbacks[name]:
            if async:
                deferd = deferToThread(func, *args, **kwargs)
                results.append(deferd)
            else:
                func(*args, **kwargs)
        return defer.DeferredList(results)


dispatch = EventDispatcher()
sub = dispatch.sub
pub = dispatch.pub
register = dispatch.register






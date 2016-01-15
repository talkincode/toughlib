#!/usr/bin/env python
# coding=utf-8

import types
class EventDispatcher:

    def __init__(self, prefix="event_"):
        self.prefix = prefix
        self.callbacks = {}


    def sub(self, name, meth):
        self.callbacks.setdefault(name, []).append(meth)


    def register(self, obj):
        from twisted.python import reflect
        d = {}
        reflect.accumulateMethods(obj, d, self.prefix)
        for k,v in d.items():
            self.sub(k, v)

    def pub(self, name, *args, **kwargs):
        for cb in self.callbacks[name]:
            cb(*args, **kwargs)


dispatch = EventDispatcher()
sub = dispatch.sub
pub = dispatch.pub
register = dispatch.register






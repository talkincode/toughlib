#!/usr/bin/env python
# coding=utf-8
import os
import types
import importlib
from twisted.internet.threads import deferToThread
from twisted.python import reflect
from twisted.internet import defer
from twisted.logger import Logger

class EventDispatcher:
    log = Logger()

    def __init__(self, prefix="event_"):
        self.prefix = prefix
        self.callbacks = {}


    def sub(self, name, func):
        self.callbacks.setdefault(name, []).append(func)
        self.log.info('register event %s --> %s' % (
            name, "{0} :: {1}".format(func.__name__,func.__doc__)))

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
                deferd.addCallbacks(lambda r:r,lambda e:e)
                results.append(deferd)
            else:
                func(*args, **kwargs)
        return defer.DeferredList(results)


dispatch = EventDispatcher()
sub = dispatch.sub
pub = dispatch.pub
register = dispatch.register

def load_events(event_path=None,pkg_prefix=None,excludes=[],event_params={}):
    _excludes = ['__init__','settings','.DS_Store'] + excludes
    evs = set(os.path.splitext(it)[0] for it in os.listdir(event_path))
    evs = [it for it in evs if it not in _excludes]
    for ev in evs:
        try:
            sub_module = os.path.join(event_path, ev)
            if os.path.isdir(sub_module):
                load_events(
                    event_path=sub_module,
                    pkg_prefix="{0}.{1}".format(pkg_prefix, ev),
                    excludes=excludes,
                    event_params=event_params,
                )
            _ev = "{0}.{1}".format(pkg_prefix, ev)
            dispatch.register(importlib.import_module(_ev).__call__(**event_params))
        except Exception as err:
            import traceback
            traceback.print_exc()
            continue





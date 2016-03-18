#!/usr/bin/env python
#coding:utf-8
from toughlib  import redis_cache
from toughlib  import storage
from twisted.trial import unittest
import sys
import os

redconf = storage.Storage(host="127.0.0.1",port=6379,passwd=None)

class SetGetTestCase(unittest.TestCase):

    def setUp(self):
        self.cache = redis_cache.CacheManager(redconf,cache_name="testcache")

    def test_set_get(self):
        self.cache.set("test:tkey","123456",10)
        _get = self.cache.get('test:tkey') 
        print _get
        assert _get == "123456"

    def test_aget(self):

        def fetch_result():
            return "b"*1024

        print self.cache.aget("test:aget",fetch_result)
        assert self.cache.get("test:aget") == "b"*1024
        assert self.cache.aget("test:aget1",fetch_result,expire=3600) == "b"*1024

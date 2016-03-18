#!/usr/bin/env python
#coding:utf-8
from toughlib  import redis_session
from toughlib  import storage
from twisted.trial import unittest
import sys
import os

redconf = storage.Storage(host="127.0.0.1",port=6379,passwd=None)
secret = '12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo='

class MockHandlerMixin:
    values = {}
    def set_secure_cookie(self,key,value):
        self.values[key] = value

    def get_secure_cookie(self,key):
        return self.values.get(key)

class RedisSessionTestCase(unittest.TestCase,MockHandlerMixin):

    def setUp(self):
        sessionManager = redis_session.SessionManager(redconf,secret,1200)
        self.session = redis_session.Session(sessionManager, self)
        

    def test_session(self):
        self.session['session_obj'] = ['test'] 
        self.session.save()
        assert self.session.get("session_obj") == ['test']



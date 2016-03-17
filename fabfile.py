#!/usr/bin/env python
import sys,os,time
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *

def test():
    local("pypy coverage run trial toughlib.tests")
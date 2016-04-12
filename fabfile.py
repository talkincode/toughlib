#!/usr/bin/env python
import sys,os,time
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughlib import __version__


env.user = 'root'
env.hosts = ['121.201.15.99']

def pub():
    try:
        local("git add . && git ci -am '%s' && git push origin master"%raw_input("commit"))
    except:
        pass
    with cd("/opt/toughlib"):
        run("git pull origin master")
        run("make upload")

def test():
    local("pypy coverage run trial toughlib.tests")
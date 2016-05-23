#!/usr/bin/env python
import sys,os,time
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughlib import __version__


env.user = 'root'
env.hosts = ['121.201.15.99']

def push():
    message = raw_input(u"input git commit message:")
    local("git add .")
    try:
        local("git commit -m \'%s: %s\'"%(__version__,message or 'no commit message'))
        local("git push origin master")
    except:
        print u'no commit'

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
#!/usr/bin/env python
# coding:utf-8 
import time
import json
from hashlib import md5
from toughlib import utils, httpclient


def make_sign(api_secret, params=[]):
    """
        >>> make_sign("123456",[1,'2',u'中文'])
        '33C9065427EECA3490C5642C99165145'
    """
    _params = [utils.safeunicode(p) for p in params if p is not None]
    _params.sort()
    _params.insert(0, secret)
    strs = ''.join(_params)
    mds = md5(strs.encode('utf-8')).hexdigest()
    return mds.upper()


def check_sign(api_secret, msg):
    """
        >>> check_sign("123456",dict(code=1,s='2',msg=u'中文',sign='33C9065427EECA3490C5642C99165145'))
        True

    """
    if "sign" not in msg:
        return False
    sign = msg['sign']
    params = [utils.safestr(msg[k]) for k in msg if k != 'sign']
    local_sign = make_sign(api_secret, params)
    return sign == local_sign

def make_message(api_secret, **params):
    """
        >>> json.loads(make_request("123456",**dict(code=1,msg=u"中文",nonce=1451122677)))['sign']
        u'58BAF40309BC1DC51D2E2DC43ECCC1A1'
    """
    if 'nonce' not in params:
        params['nonce' ] = str(int(time.time()))
    params['sign'] = make_sign(api_secret, params.values())
    return json.dumps(params, ensure_ascii=False)

def make_error(api_secret, msg=None):
    """
        >>> json.loads(make_error("123456",msg="error")['sign']
        u'58BAF40309BC1DC51D2E2DC43ECCC1A1'
    """
    params = dict(code=1, msg=msg)
    params['nonce' ] = str(int(time.time()))
    params['sign'] = make_sign(api_secret, params.values())
    return json.dumps(params, ensure_ascii=False)


def parse_request(api_secret, reqbody):
    """
        >>> parse_request("123456",'{"nonce": 1451122677, "msg": "helllo", "code": 0, "sign": "DB30F4D1112C20DFA736F65458F89C64"}')
        {u'nonce': 1451122677, u'msg': u'helllo', u'code': 0, u'sign': u'DB30F4D1112C20DFA736F65458F89C64'}
    """
    try:
        req_msg = json.loads(reqbody)
    except Exception as err:
        raise ValueError(u"parse params error")

    if not check_sign(api_secret, req_msg):
        raise ValueError(u"message sign error")

    return req_msg

def request(apiurl, data=None, **kwargs):
    headers = {"Content-Type": ["application/json"]}
    return httpclient.post(apiurl, data=data, **kwargs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    
# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-06 12:15:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
from __future__ import absolute_import
import os
import sys
import redis
import json
from cottle import handle

name = 'redis'

RHOST = '127.0.0.1'
RPORT = 6379
RDB   = 0
class index(handle):
    def GET(self):
        return self.template('redis')

class Set(handle):
    def GET(self):
        return json.dumps((RHOST, RPORT, RDB))

class KEYS(handle):
    def GET(self):
        red = redis.Redis(port = RPORT, host = RHOST, db = RDB)
        return json.dumps(red.keys())

class KEYS_KEY(handle):
    def GET(self, key):
        red = redis.Redis(port = RPORT, host = RHOST, db = RDB)
        t = red.type(key)
        res = {'type': t, 'value': None}
        if t == 'none':
            res['value'] = None

        if t == 'hash':
            res['value'] = red.hgetall(key)

        if t == 'string':
            res['value'] = red.get(key)
        return json.dumps(res)


urls = (
        'Set', Set,
        '/', index,
        "/KEYS", KEYS,
        "/KEYS/(.+)", KEYS_KEY,
        )


if __name__ == "__main__":
    pass


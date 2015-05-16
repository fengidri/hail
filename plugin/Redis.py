# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-06 12:15:59
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import sys
import redis
import json
from cottle import handle

name = 'redis'

class index(handle):
    def GET(self):
        return self.template('redis')

class RedisOptions(handle):
    def Before(self):
        host = self.params[0]
        port = self.params[1]
        db   = self.params[2]

        try:
            self.red = redis.Redis(port = port, host = host, db = db)
        except:
            self.abort(500, '%s/%s/%s Error' % (host, port, db))
        return True

    def After(self):
        del self.red

class KEYS(RedisOptions):
    def GET(self):
        _filter = self.query.get("filter", "*")

        try:
            data = self.red.keys(_filter)
            return {"status":True, "data":data}

        except:
            return {"status":False}


class KEYS_KEY(RedisOptions):
    def GET(self):
        red = self.red
        key = self.params[-1]
        t = red.type(key)

        value = None
        if t == 'hash':
            value = red.hgetall(key)

        if t == 'string':
            value = red.get(key)

        if t == 'set':
            value = red.smembers(key)

        if t == 'list':
            value = red.lrange(key, 0, -1)

        if t == 'zset':
            value = red.zrange(key, 0, -1)

        res = {'type': t, 'value': value}
        return json.dumps(res, ensure_ascii=False)


class DB(RedisOptions):
    def DELETE(self):
        red = self.red
        red.flushdb()
        return "ok"


urls = (
        '/', index,
        "/([^/]+)/([^/]+)/([^/]+)/KEYS", KEYS,
        "/([^/]+)/([^/]+)/([^/]+)/KEYS/(.+)", KEYS_KEY,
        "/([^/]+)/([^/]+)/([^/]+)/DB", DB,
        )


if __name__ == "__main__":
    pass


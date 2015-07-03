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
from textohtml import texstohtmls
import traceback

name = 'autofresh'
urls = ('', "index",
        '/data', "data")

class index(handle):
    def GET(self):
        return self.template('autofresh')

class data(handle):
    data = "-- no data --"
    tp   = ''
    index = 0
    def GET(self):
        qindex = self.query.get("index")
        if qindex and qindex == str(self.index):
            return [self.index, '']
        data = self.data
        if self.tp in ['mkiv', 'content']:
            try:
                data = texstohtmls(self.data)
            except:
                data = "<pre>%s</pre>" % traceback.format_exc()
        return [self.index, data]

    def POST(self):
        self.tp    =  self.forms.get('type')
        self.data  =  self.forms.get('data')
        self.index += 1
        return 'OK'


if __name__ == "__main__":
    pass

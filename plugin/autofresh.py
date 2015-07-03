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
    data = "--no data--"
    def GET(self):
        return self.data

    def POST(self):
        tp = self.forms.get('type')
        self.data = self.forms.get('data')
        if tp in ['mkiv', 'content']:
            try:
                self.data = texstohtmls(self.data)
            except:
                self.data = "<pre>%s</pre>" % traceback.format_exc()
        return 'OK'


if __name__ == "__main__":
    pass

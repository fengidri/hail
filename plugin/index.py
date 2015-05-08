# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-06 18:30:36
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from cottle import handle
name = ''
urls = (
        '', "index",
        )
class index(handle):
    def GET(self):
        return self.template('index')

if __name__ == "__main__":
    pass


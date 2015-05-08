# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-06 18:36:01
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from cottle import handle
name = 'json'
urls = (
        '', "index",
        )

class index(handle):
    def GET(self):
        return self.template('json')


if __name__ == "__main__":
    pass


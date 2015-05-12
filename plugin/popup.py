# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-12 11:53:07
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
name = 'popup'
urls = ('/(.*)', 'show')

from cottle import handle
class show(handle):
    def GET(self):
        return self.template('popup')



if __name__ == "__main__":
    pass


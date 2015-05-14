# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-14 10:27:34
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

urls = ('', 'proxy')
from cottle import handle
import urllib2
class proxy(handle):
    def POST(self):
        #self.forms.get('method')
        url = self.forms.get('url')
        return urllib2.urlopen(url).read()

if __name__ == "__main__":
    pass


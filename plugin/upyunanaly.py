# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-28 11:36:26
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

from cottle import handle
import os
import json
import time
import subprocess
import tempfile

name = 'upyun'
urls = (
        '/analy', "index",
        '/test', 'test',
        )


class Header(object):
    def __init__(self, header):
        self.header = header

    def get_header(self, k):
        k = k.lower()
        for item in self.header:
            if k == item.get('name', '').lower():
                return item.get('value', '')

class Request(Header):
    def __init__(self, req):
        self.method      = req.get('method')
        self.url         = req.get('url')
        self.httpversion = req.get('httpversion')
        self.cookies     = req.get('cookies')
        self.query       = req.get('queryString')

        Header.__init__(self, req.get('headers'))

    def get_host(self):
        url = self.url
        if url.startswith('https'):
            url = url[8:]
        else:
            url = url[7:]
        return url.split('/', 1)[0]

class Response(Header):
    def __init__(self, res):
        self.status      = res.get('status')
        self.msg         = res.get('statusText')
        self.httpversion = res.get('httpversion')
        self.cookies     = res.get('cookies')
        self.redirectURL = res.get('redirectURL')
        self.bodySize    = res.get('bodySize')
        Header.__init__(self, res.get('headers'))



class Timing(object):
    def __init__(self, timing):
        self.timing = timing

class ReSource(object):
    def __init__(self, resource):
        self.startedDateTime = resource.get('startedDateTime')
        self.loadtime        = resource.get('time')
        self.pageref         = resource.get('pageref')

        self.timing          = Timing(resource.get('timing'))
        self.req             = Request(resource.get('request'))
        self.res             = Response(resource.get('response'))

    def is_gzip(self):
        c = self.res.get_header('Content-Encoding')
        if not c:
            return False
        if c.lower().find('gzip') > -1:
            return True
        else:
            return False

    def is_upyun_cdn(self):
        s = self.res.get_header('Server')
        if not s:
            return False
        if s.lower().startswith('marco'):
            return True
        else:
            return False

    def is_cdn_hit(self):
        s = self.res.get_header('X-Cache')
        if not s:
            return False
        if s.find('HIT') > -1:
            return True
        else:
            return False
    def is_https(self):
        if self.req.url.startswith('https'):
            return True
        return False

class HAR(object):
    def __init__(self, url):
        self.tmpfile = tempfile.mktemp()
        cmd = 'cd /home/feng/phantomjs; phantomjs netsniff.js %s > %s' % (url,
                self.tmpfile)
        print cmd
        self.p = subprocess.Popen(cmd, shell=True)
        self.inited = False

    def poll(self):
        if self.inited:
            return 0
        res = self.p.poll()
        if None == res:
            return None

        if self.p.returncode != 0:
            return -1


        #har = self.p.communicate()[0]
        har = open(self.tmpfile).read()
        har = json.loads(har)
        self.init(har)
        return 0

    def init(self, _har):
        self.inited = True
        har = _har.get('log')

        self.render   = _har.get('render')

        page          = har.get('pages')[0]
        self.url      = page.get('id')
        self.title    = page.get('title')
        self.loadtime = page.get('pageTimings').get('onLoad')

        self.resources = []
        for h in har.get('entries'):
            self.resources.append(ReSource(h))

    def get_render(self):
        return self.render

    def get_resource_num(self):
        return len(self.resources)

    def get_recv_size(self):
        t = 0
        for r in self.resources:
            if r.res.bodySize > 0:
                t += r.res.bodySize
        return t

    def get_resource_list(self):
        ls = []
        for r in self.resources:
            res = r.res
            req = r.req
            t = [req.url, res.bodySize,  r.loadtime]
            ls.append(t)
        return ls


    def get_analy(self):
        total_cdn = 0
        total_gzip = 0
        total_hosts = []
        total_hit = 0
        total_https = 0
        status = {}

        for r in self.resources:
            if r.is_upyun_cdn():
                total_cdn += 1
                if r.is_cdn_hit():
                    total_hit += 1

            if r.is_gzip():
                total_gzip += 1

            if r.is_https():
                total_https += 1

            if status.get(r.res.status):
                status[r.res.status] += 1
            else:
                status[r.res.status] = 1

            total_hosts.append(r.req.get_host())

        return {
                'cdn': total_cdn,
                'gzip': total_gzip,
                'hit': total_hit,
                'loadtime': self.loadtime,
                'total': self.get_resource_num(),
                'size': self.get_recv_size(),
                'hosts': len(set(total_hosts)),
                'https': total_https,
                'codes': status,
                }



class index(handle):
    def GET(self):
        return self.template('upyun_analy')


class test(handle):
    HARS = {}
    TEST_ID = time.time()

    def makeid(self):
        self.TEST_ID += 1
        return str(self.TEST_ID)

    def GET(self):
        ID = self.query.get("ID")
        if not ID:
            self.abort(400, 'Not Found. ID')

        har = self.HARS.get(ID)
        if har == None:
            self.abort(400, 'Not Found HAR for %s' % ID)

        if None == har.poll():
            return {'status', 'waiting'}

        if -1 == har.poll():
            return {'status', 'error'}

        _ = self.query.get('_')

        if _ == 'analy':
            analy = har.get_analy()
            analy['status']= 'complete'
            return analy

        if _ == 'render':
            path = har.get_render()
            png = os.path.basename(path)
            root = os.path.dirname(path)
            return self.cfile(png, root)

        if _ == 'resource':
            return har.get_resource_list()


    def POST(self):
        ID = self.makeid()

        url = self.forms.get('url')
        self.HARS[ID] = HAR(url)

        return ID




if __name__ == "__main__":
    pass


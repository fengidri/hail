# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-14 22:05:50
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
import context2 as context
from cottle import  handle
import wiki.modules as dw       #data of wiki
import urllib2

STOREPATH = os.path.join(os.getcwd(), 'submodules/fengidri.github.io/store')
WIKIPATH = os.path.join(os.getcwd(), 'submodules/fengidri.github.io')
dw.init(STOREPATH)

name = 'fwiki'
urls = (
    '/chapters', 'chapters',
    '/chapters/(\d+)', 'chapter',
    '/(.*)', 'index',
        )

class index(handle):# 提供静态网页功能
    def GET(self, filename):
        return self.cfile(filename, WIKIPATH)



class chapters(handle):
    def POST(self):
        title   = self.forms.get('title')
        content = self.forms.get('content')
        cls    = self.forms.get('class',    '')
        public = int(self.forms.get('post', 1))
        tags   = self.forms.get('tags',     [])
        res     = dw.add(title, content, cls, tags, public)
        dw.save()
        return res

    def GET(self):#返回列表
        c = self.env.get('HTTP_ACCEPT', 'text/html')
        ll = dw.list()
        if c.find('json') > -1:
            return ll
        else:
            file_list = []
            total_nu = len(ll)
            for index in ll:
                c = dw.get(index)
                file_list.append((c.title, index))
                
            return self.template("wiki_index", locals())

class chapter(handle):
    def get_filename(self, field):
        e = self.env.get(field, 'text/html')
        for tt in e.split(';'):
            kv = tt.split('=')
            if len(kv) == 2:
                k,v = kv
                if k.strip() == 'filename':
                    return v.strip()
        else:
            return self.query.get('filename', 'index.mkiv')

    def GET(self,  Id):
        Id = int(Id)
        chapter = dw.get(Id)
        if not chapter:
            self.abort(404)
        fn = self.get_filename('HTTP_ACCEPT')

        c = self.env.get('HTTP_ACCEPT', 'text/html')
        if c.find('text/json+mkiv') > -1:# 返回mkiv 文件的内容
            f = chapter.read(fn)
            if not f:
                self.abort(404)
            return {'name':chapter.title, 'content': f[1], 'filename':f[0],
                    'ID': Id}
        elif c.find('text/json+files') > -1:# 返回chapter 的files 信息
            return chapter.list()
        else:
            w = context.context2htmls(chapter.read(fn)[1].decode('utf8'))
            return self.template("show_wiki", wiki= w, 
                    title =chapter.title, ID=Id)

    def PUT(self,  Id):
        Id = int(Id)
        chapter = dw.get(Id)
        if not chapter:
            self.abort(404)

        title = self.forms.get('title')
        if title:
            chapter.settitle(title)
        
        cls = self.forms.get('class')
        if cls:
            chapter.setcls(cls.decode('utf8'))
        
        tag = self.forms.get('tags')
        if tag:
            chapter.settag(tag.split(','))

        p = self.forms.get('post')
        if p != None:
            if p == '0' or p.lower() == 'false':
                p = False
            else:
                p = True 
            chapter.setpublic(p)

        #content
        content = self.forms.get('content')
        url = self.forms.get('url')
        if not content and url:# 只在没有content 的情况下检查url
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'http://%s' % url
            content = urllib2.urlopen(url).read() # 从url 读取数据
        if content:
            chapter.write(self.get_filename("HTTP_CONTENT_TYPE"),  content)


        fn = self.forms.get('delete')
        if fn:
            if not chapter.delfn(fn):
                self.abort(404)

        dw.save()
        return Id

    def DELETE(self, Id):
        Id = int(Id)
        chapter = dw.get(Id)
        if not chapter:
            self.abort(404)
        chapter.delete()
        dw.save()
        return Id



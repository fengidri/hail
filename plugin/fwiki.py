# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-14 22:05:50
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

# 本模块只提供blog 信息的数据修改, 并不提供读取分析功能

import os
from cottle import  handle
from wiki.modules import BlogDate       #data of wiki


STOREPATH = os.path.join(os.getcwd(), '../blog/store')
STOREPATH = os.path.join(os.getcwd(), 'submodules/fengidri.github.io/store')
STOREPATH = os.path.join(os.getcwd(), '/var/www/blog/store')

name = 'fwiki'
urls = (
    '/chapters', 'chapters',
    '/chapters/(\d+)', 'chapter',
        )




class chapters(handle):
    def POST(self):
        dw = BlogDate(STOREPATH)
        title    = self.forms.get('title')
        tex  = self.forms.get('tex')
        html = self.forms.get('html')
        cls      = self.forms.get('class',    '')
        public   = int(self.forms.get('post', 1))
        tags     = self.forms.get('tags',     [])
        res      = dw.add(title, tex, html, cls, tags, public)
        dw.save()
        return res

class chapter(handle):
    def PUT(self,  Id):
        dw = BlogDate(STOREPATH)

        Id = int(Id)
        chapter = dw.getchapter(Id)
        if not chapter:
            self.abort(404)

        save = False

        title = self.forms.get('title')
        if title:
            save = True
            chapter.settitle(title)
        
        cls = self.forms.get('class')
        if cls:
            save = True
            chapter.setcls(cls.decode('utf8'))
        
        tag = self.forms.get('tags')
        if tag:
            save = True
            chapter.settag(tag.split(','))

        p = self.forms.get('post')
        if p != None:
            if p == '0' or p.lower() == 'false':
                p = False
            else:
                p = True 
            save = True
            chapter.setpublic(p)

        tex = self.forms.get('tex')
        html = self.forms.get('html')
        if tex and html:
            chapter.write(tex, html)

        if save:
            dw.save()
        return Id



# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-15 20:26:30
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
import os
curdir = os.path.dirname(os.path.realpath(__file__))

plugin_path = os.path.join(curdir, 'plugin')
site_packages = os.path.join(curdir, 'site-packages')



import sys
sys.path.insert(0, site_packages)

import json
import logging
import re
import types

import web
import plugins
import cottle
PLUGINS = []
URLS = [] 

def load_plugin(plugin_path):
    ps = plugins.load(plugin_path, 'name', 'urls')
    for mode, name, urls in ps.values():
        mode_init(mode, name, urls)
def mode_init(mode, name, urls):
    for url, fun in list(web.utils.group(urls, 2)):
        url = '/%s%s' % (name, url)
        
        if isinstance(fun, basestring):
            if not hasattr(mode, fun):
                logging.error('plugin %s not hasattr [%s]' % (modename, fun))
                continue
            fun = getattr(mode, fun)

        URLS.append((url,fun))
    PLUGINS.append((name,mode))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s'
    #       ,filename="/home/log/voscfg/voscfg.log"
            )

    logging.info('start cfg......')

    load_plugin(plugin_path)

    for u,c in web.utils.group(URLS, 2):
        logging.info("%s:%s" % (u,c))
    app = application(tuple(URLS), globals())
    app.run()
else:#uwsgi
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s'
    #       ,filename="/home/log/voscfg/voscfg.log"
            )

    logging.info('start cfg......')

    load_plugin(plugin_path)

    for u,c in URLS:
        logging.info("%s:%s" % (u,c))
    application = app = cottle.cottle.app()
    app.setroot('static')
    app.mapping.load(tuple(URLS), globals())

#class application(web.application):
#    def handle(self):
#        fn, args = self._match(self.mapping, web.ctx.path)
#
##        if web.ctx.method == 'POST':
##            if web.ctx.env.get('CONTENT_TYPE') == 'application/json':
##                try:
##                    j = json.loads(web.data())
##                except:
##                    web.ctx.status = "500 json load error"
##                    return web.ctx.status
##                a = [None, j]
##            else:
##                a = web.input()
##        else:
##            a = [web.input()]
##        if args == None:
##            args = [a]
##        else:
##            args.insert(0, a)
##
#        res =  self._delegate(fn, self.fvars, args)
#        if isinstance(res, web.template.TemplateResult):
#            return res
#        if not isinstance(res, basestring):
#            res = json.dumps(res)
#        return res
#
#    def _delegate(self, f, fvars, args=[]):
#        def handle_class(cls):
#            meth = web.ctx.method
#            if meth == 'HEAD' and not hasattr(cls, meth):
#                meth = 'GET'
#            if not hasattr(cls, meth):
#                raise web.nomethod(cls)
#            co = cls()
#
#            print web.forms()
#            print web.query()
#            if meth in ['POST', 'PUT']:
#                co.forms = web.forms()
#            co.query = web.query()
#
#            tocall = getattr(co, meth)
#            return tocall(*args)
#            
#        def is_class(o): return isinstance(o, (types.ClassType, type))
#            
#        if f is None:
#            raise web.notfound()
#        elif isinstance(f, web.application):
#            return f.handle_with_processors()
#        elif is_class(f):
#            return handle_class(f)
#        elif isinstance(f, basestring):
#            if f.startswith('redirect '):
#                url = f.split(' ', 1)[1]
#                if web.ctx.method == "GET":
#                    x = web.ctx.env.get('QUERY_STRING', '')
#                    if x:
#                        url += '?' + x
#                raise web.redirect(url)
#            elif '.' in f:
#                mod, cls = f.rsplit('.', 1)
#                mod = __import__(mod, None, None, [''])
#                cls = getattr(mod, cls)
#            else:
#                cls = fvars[f]
#            return handle_class(cls)
#        elif hasattr(f, '__call__'):
#            return f()
#        else:
#            return web.notfound()
##class application(web.application):
##    def handle(self):
##        fn, args = self._match(self.mapping, web.ctx.path)
##        if web.ctx.method == "POST":
##            post = web.input().get("JSON")
##            if post:
##                try:
##                    post = json.loads(post)
##                except:
##                    logging.error('JSON loads error: %s' % post)
##                    post =None
##            else:
##                logging.error('post no found JSON')
##            args.insert(0, post)
##        res = self._delegate(fn, self.fvars, args)
##        if isinstance(res, web.template.TemplateResult):
##            return res
##        if not isinstance(res, basestring):
##            res = json.dumps(res)
##        return res

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
        if url.startswith('/'):
            url = '/%s%s' % (name, url)
        else:
            url = os.path.join('/', name, url)

        
        if isinstance(fun, basestring):
            if not hasattr(mode, fun):
                logging.error('plugin %s not hasattr [%s]' % (mode, fun))
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
    application = app = cottle.app()
    app.setroot('static')
    app.mapping.load(tuple(URLS), globals())


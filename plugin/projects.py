# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-12-05 16:04:10
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
name = 'projects'
urls = (
        '/index', 'index',
        '/configs', 'configs',
        '/configs/([^/]+)', 'config',
        '/runtimes/([^/]+)', 'config')

home = os.environ[ "HOME" ]

config_dir = os.path.join(home, '.config/mescin')
runtime_dir = os.path.join( config_dir, '.runtime' )
def init():
    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)
    if not os.path.isdir(runtime_dir):
        os.mkdir(runtime_dir)
init()

class index:
    def GET(self):
        return self.template('projects')

class configs:
    def GET(self):
        cfg_files = os.listdir( config_dir )
        return [ x for x in cfg_files if x.endswith('.json')]


    def POST(self):
        content = self.forms.get('content')
        name = self.forms.get('name')
        path = os.path.join(config_dir, name)
        open(path).write(content)
        return 'OK'


class config:
    cpath = config_dir
    def GET(self, name):
        path = os.path.join(self.cpath, name)
        self.response.set_content_json()

        return open(path).read()

    def PUT(self, name):
        content = self.forms.get('content')
        path = os.path.join( self.cpath, name )
        open(path).write(content)
        return 'OK'

    def DELETE(self, name):
        p = os.path.join(self.cpath, name)
        if not os.path.isfile(p):
            self.abort(404)
        os.remove(p)
        return 'OK'

class runtime(config):
    cpath = config_dir


if __name__ != "__main__":
    pass
    


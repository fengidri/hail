# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-08 15:17:19
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import time
from Email import Email
from cottle import handle

def td_add(em, todo):
    em.Msg('TODOLIST', todo)
    em.Send()

def td_get(em, done = False):
    em.mailbox = 'TODOLIST'
    if done == True:
        criterion = 'seen'
    else:
        criterion = 'Unseen'

    ids = em.Search(criterion)
    if not ids:
        return []

    es = em.Fetch(ids)
    todos = []
    for ID, e in es:
        for part in e.walk():
            # multipart/* are just containers
            if part.get_content_maintype() == 'multipart':
                continue
            msg = part.get_payload(decode=True)
        d = ' '.join(e['date'].split()[0:5])
        d = time.strptime(d, "%a, %m %b %Y %H:%M:%S")
        d = time.strftime("%Y-%m-%d %H:%M:%S %a")

        todos.append((d, msg, ID))
    return todos

name = "todo"
urls = (
'', 'index',
'/index', 'index',
        '/set', 'Set',
        '/todo', 'TODOs'

        )

class todo(handle):
    def Before(self):
        smtphost = self.getcookie('SMTP')
        imaphost = self.getcookie('IMAP')
        pwd      = self.getcookie('pwd')
        user     = self.getcookie('user')
        if not (smtphost and imaphost and pwd and user):
            self.redirect('/todo/set')
        print smtphost, imaphost, pwd, user

        self.em = Email(smtphost, imaphost, user, user, pwd)
        return True

    def After(self):
        self.em = None

class Set(handle):
    def GET(self):
        return self.template("todo_set")

class index(todo):
    def GET(self):
        return self.template("todo_list")

class TODOs(todo):
    def GET(self):
        return td_get(self.em)

    def POST(self):
        td_add(self.em, self.forms.get('todo'))
        self.redirect('/todo/index')


if __name__ == "__main__":
    pass


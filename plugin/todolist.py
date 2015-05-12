# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-05-08 15:17:19
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import time
from Email import Email
from cottle import handle


from imapclient import IMAPClient


from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email.encoders import encode_base64
import email
class Message(object):
    def __init__(self):
        self.status = 'open'
        self.flag = []
        self.msg = ''
        self.data = None


class MsgItem(object):
    def __init__(self, HOST, USERNAME, PASSWORD, ssl=False,
            folder='TODOLIST'):

        imap = IMAPClient(HOST, use_uid=True, ssl=ssl)
        imap.login(USERNAME, PASSWORD)

        try:
            imap.select_folder(folder)
        except imap.Error, e:
            imap.create_folder(folder)

        self.imap = imap
        self.folder = folder
        self.user = USERNAME

    def AddItem(self, subject, msg = ''):
        f =  MIMEBase('MsgItem', 'item')
        f['Subject'] = Header(subject, 'UTF-8')
        f['From']    = self.user
        f['To']      = self.user
        f.set_payload(msg)
        encode_base64(f)

        print  self.imap.append(self.folder, f.as_string())


    def CloseItem(self, msgid=None, uid=None):
        if uid:
            msgid = self.UidToMsgId(uid)

        if not isinstance(msgid, list):
            msgid = [msgid]

        for ID in msgid:
            f =  MIMEBase('MsgItem', 'option')
            f['Subject']       = Header('option', 'UTF-8')
            f['From']          = self.user
            f['To']            = self.user
            f['Reply-To']      = self.user
            f['In-Reply-To']   = ID
            f['X-Item-Status'] = 'close'
            encode_base64(f)

            msg = f.as_string()

            self.imap.append(self.folder, msg)

    def ListUidItem(self, f = ['NOT DELETED']):
        return self.imap.search(f)

    def ListItem(self, status = 'open'):
        ids = self.imap.search(['NOT DELETED'])
        ems = self.Fetch(ids)
        print len(ems)

        todos = []
        for uid, e in ems.items():
            e  = email.message_from_string(e['RFC822'])
            for part in e.walk():
                # multipart/* are just containers
                if part.get_content_maintype() == 'multipart':
                    continue
                msg = part.get_payload(decode=True)

            t = e['received'].split(';')[-1]

            d = ' '.join(t.split()[0:5])
            d = time.strptime(d, "%a, %m %b %Y %H:%M:%S")
            d = time.strftime("%Y-%m-%d %H:%M:%S %a")
            print msg, d
            todos.append((d, msg, uid))
        print todos
        return todos






    def UidToMsgId(self, uid):
        if not isinstance(uid, list):
            uid = [uid]
        res = self.Fetch(uid, ['RFC822.HEADER'])
        msgid = []
        for i in uid:
            headers = email.message_from_string(res[i]['RFC822.HEADER'])
            msgid.append(headers['Message-Id'])
        return msgid


    def Fetch(self, uid, data = ['RFC822']):
        return self.imap.fetch(uid, data )






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
        imaphost = self.getcookie('IMAP')
        pwd      = self.getcookie('pwd')
        user     = self.getcookie('user')
        if not (imaphost and pwd and user):
            self.redirect('/todo/set')

        self.em = MsgItem(imaphost, user, pwd)
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
        return self.em.ListItem()

    def POST(self):
        self.em.AddItem('TODO', self.forms.get('todo'))
        self.redirect('/todo/index')
        raise


if __name__ == "__main__":
    pass


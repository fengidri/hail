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
import email.utils

class Emsg(object):
    def decode(self, h):
        _h = u''
        for m, charset in decode_header(h):
            if charset == None:
                _h += m
            else:
                _h += m.decode(charset)
        return _h

    def __init__(self, msg):
        self.msg = email.message_from_string(msg)

    def _addrs(self, addrs):
        addrlist = []
        regex = "(^.*)<(.*)>"
        for addr in addrs.split(','):
            addr = addr.strip()
            match = re.search(regex, addr)
            if not match:
                infolist.append((addr.split('@')[0], addr))
            else:
                name = self.decode(match.group(1))
                addr = match.group(2)
                addrlist.append((name, addr))
        return addrlist

    def Header(self, field):
        return self.msg[field]

    @property
    def Subject(self):
        return self.decode(self.msg['Subject'])

    @property
    def To(self):
        return self._addrs(self.msg['To'])

    @property
    def From(self):
        return self._addrs(self.msg['From'])

    @property
    def Cc(self):
        if cc == self.msg['Cc']:
            return self._addrs(cc)
        else:
            return []
    @property
    def MsgId(self):
        return self.msg['Message-Id']

    @property
    def InReplyTO(self):
        return self.msg['In-Reply-To']

    @property
    def Date(self):
        d = self.msg['Date']
        if not d:
            d = self.msg['Received'].split(';')[-1].strip()

        return time.mktime(email.utils.parsedate(d))

    @property
    def Msg(self):
        ms = []
        for part in self.msg.walk():
            ms.append(part)
            # multipart/* are just containers
            #if part.get_content_maintype() == 'multipart':
            #    continue
            #msg = part.get_payload(decode=True)
        return ms

class Message(Emsg):
    def __init__(self, uid, msg):
        Emsg.__init__(self, msg['RFC822'])
        self.uid = uid

    @property
    def Msg(self):
        for part in self.msg.walk():
             #multipart/* are just containers
            if part.get_content_maintype() == 'multipart':
                continue
            msg = part.get_payload(decode=True)
        return msg


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

        todos = {}
        reply = []
        for uid, e in ems.items():
            m = Message(uid, e)

            if m.InReplyTO:
                reply.append(m)
            else:
                todos[m.MsgId] = m

        for r in reply:
            print '***********', r
            del todos[r.InReplyTO]

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






name = "todo"
urls = (
'', 'index',
'/index', 'index',
'/set', 'Set',
'/todo', 'TODOs',
'/todo/(\d+)', 'Option'

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
        todos = []
        for td in self.em.ListItem().values():
            todos.append((td.uid, td.Msg, '1'))
        return todos

    def POST(self):
        self.em.AddItem('TODO', self.forms.get('todo'))
        self.redirect('/todo/index')

class Option(todo):
    def PUT(self):
        uid = int(self.params[0])
        self.em.CloseItem(uid = uid)
        self.redirect('/todo/index')


if __name__ == "__main__":
    pass


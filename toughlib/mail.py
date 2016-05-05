#!/usr/bin/env python
#coding:utf-8

from cStringIO import StringIO
from OpenSSL.SSL import SSLv3_METHOD
from twisted.mail.smtp import ESMTPSenderFactory
from twisted.internet.ssl import ClientContextFactory
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from toughlib import  utils
from toughlib import dispatch,logger
from twisted.mail.smtp import sendmail
# from email.mime.text import MIMEText
# from email import Header
import email

class SendMail:

    def __init__(self, server='127.0.0.1', port=25, user=None, password=None,from_addr=''):
        self.smtp_server = utils.safestr(server)
        self.from_addr = utils.safestr(from_addr)
        self.smtp_port = int(port)
        self.smtp_user = user
        self.smtp_pwd = password

    def send_mail(self, mailto, topic, content, tls=False,**kwargs):
        message = email.MIMEText.MIMEText(content,'html', 'utf-8')
        message["Subject"] = email.Header.Header(topic,'utf-8')
        message["From"] = email.Header.Header("%s <%s>"%(self.from_addr[:self.from_addr.find('@')],self.from_addr),'utf-8')
        message["To"] = mailto
        message["Accept-Language"]="zh-CN"
        message["Accept-Charset"]="ISO-8859-1,utf-8"
        if not tls:
            logger.info('send mail')
            return sendmail(self.smtp_server, self.from_addr, mailto, message,
                        port=self.smtp_port, username=self.smtp_user, password=self.smtp_pwd)
        else:
            logger.info('send tls mail')
            contextFactory = ClientContextFactory()
            contextFactory.method = SSLv3_METHOD
            resultDeferred = Deferred()
            senderFactory = ESMTPSenderFactory(
                self.smtp_user,
                self.smtp_pwd,
                self.from_addr,
                mailto,
                StringIO(message.as_string()),
                resultDeferred,
                contextFactory=contextFactory,
                requireAuthentication=(self.smtp_user and self.smtp_pwd),
                requireTransportSecurity=tls)

            reactor.connectTCP(self.smtp_server, self.smtp_port, senderFactory)
            return resultDeferred


def send_mail(server='127.0.0.1', port=25, user=None, password=None, 
                from_addr=None, mailto=None, topic=None, content=None, tls=False, **kwargs):
    sender = SendMail(server,port,user,password,from_addr)
    return sender.send_mail(mailto, topic, content, tls=tls,**kwargs)











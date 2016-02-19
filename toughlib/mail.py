#!/usr/bin/env python
#coding:utf-8

from toughlib import  utils
from toughlib import dispatch,logger
from twisted.mail.smtp import sendmail
from email.mime.text import MIMEText
from email import Header

class SendMail:

    def __init__(self, server='127.0.0.1', port=25, user=None, password=None,from_addr=None):
        self.smtp_server = server
        self.from_addr = from_addr
        self.smtp_port = port
        self.smtp_user = user
        self.smtp_pwd = password

    def send_mail(self, mailto, topic, content, **kwargs):
        message = MIMEText(content,'html', 'utf-8')
        message["Subject"] = Header(topic,'utf-8')
        message["From"] = Header("%s <%s>"%(fromaddr[:fromaddr.find('@')],fromaddr),'utf-8')
        message["To"] = mailto
        message["Accept-Language"]="zh-CN"
        message["Accept-Charset"]="ISO-8859-1,utf-8"
        if '@toughradius.org' in fromaddr:
            message['X-Mailgun-SFlag'] = 'yes'
            message['X-Mailgun-SScore'] = 'yes'

        return sendmail(self.smtp_server, self.from_addr, mailto, message,
                        port=self.smtp_port, username=self.smtp_user, password=self.smtp_pwd)


def send_mail(server='127.0.0.1', port=25, user=None, password=None, 
                from_addr=None, mailto=None, topic=None, content=None, **kwargs):
    return SendMail(server,port,user,password,from_addr).send_mail(mailto, topic, content, **kwargs)




#!/usr/bin/python
import smtplib
import os
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64
import difflib
import subprocess
import simplejson as json
import urllib2
import urllib

emailAddress = '' #Enter your email address here
emailPassword = '' #Enter your password here
recipient = '' #Enter the recipient here
smtpaddress = 'smtp.gmail.com'#Enter SMTP address of mail server here
    
###########################################################
# mailicious - a script to send email updates for HN      #
#    written by Arvin A                                   #
#                                                         #
# Last revised 2013-01-13                                 #
#                                                         #
# This software is licensed under the GPLv2               #
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html   #
###########################################################


class Story(object):
    def __init__(self, **kwargs):
       self.id =  kwargs['id']
       self.url = kwargs['url']
       self.title = kwargs['title']
       self.username = kwargs['postedBy']
       self.timestamp = kwargs['postedAgo']
    def __str__(self):
       return self.title + "\n" + self.url

def sendMail(subject, text, *attachmentFilePaths):
    global emailAddress, emailPassword, recipient, smtpaddress
    msg = MIMEMultipart()
    msg['From'] = emailAddress
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    mailServer = smtplib.SMTP(smtpaddress, 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(emailAddress, emailPassword)
    mailServer.sendmail(emailAddress, recipient, msg.as_string())
    mailServer.close()

data = json.load(urllib.urlopen("http://api.ihackernews.com/page"))
items = list()
for item in data['items']:
    story = Story(id=item['id'], url=item['url'], title=item['title'], postedBy=item['postedBy'], postedAgo=item['postedAgo'])
    items.append(story)
text = ""
for item in items:
    text = text + "\n" + str(item)
sendMail("HN Update", text, None)

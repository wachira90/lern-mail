#!/usr/bin/env python

import smtplib, ssl
from email.mime.text import MIMEText

sender = 'admin@example.com'
receivers = ['info@example.com']

port = 465
user = 'admin@example.com'
password = 'password'

msg = MIMEText('This is test mail')

msg['Subject'] = 'Test mail'
msg['From'] = 'admin@example.com'
msg['To'] = 'info@example.com'

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.websupport.sk", port, context=context) as server:

    server.login(user, password)
    server.sendmail(sender, receivers, msg.as_string())
    print('mail successfully sent')

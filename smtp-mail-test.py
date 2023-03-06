#!python
import smtplib
'''
python3 smtp
'''

sender = 'user@example.com'
receivers = ['to_user@example.com']
passwd = 'xxxxx'

message = """From: User <user@example.com>
To: to_user <to_user@example.com>
Subject: SMTP e-mail test
This is a test e-mail message.
"""

try:
    mailserver = smtplib.SMTP('smtp.office365.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(sender, passwd)
    mailserver.sendmail(sender, receivers, message)
    mailserver.quit()
except :
    print ("Error: unable to send email")

# Test mail debug python

Python 3.7.4

## run debug server

````
python -m smtpd -c DebuggingServer -n localhost:1025
````

## code 

````
#!python
import smtplib
from email.mime.text import MIMEText

sender = 'admin@example.com'
receivers = ['info@example.com']


port = 1025
msg = MIMEText('This is test mail')

msg['Subject'] = 'Test mail'
msg['From'] = 'admin@example.com'
msg['To'] = 'info@example.com'

with smtplib.SMTP('localhost', port) as server:
    
    # server.login('username1111', 'password1111')
    server.sendmail(sender, receivers, msg.as_string())
    print("Successfully sent email")
````

## run server debug

````
python -m smtpd -c DebuggingServer -n localhost:1025
````

## run 

````
C:\testmail>python mail-send.py
Successfully sent email
````

## result

````
D:\>python -m smtpd -c DebuggingServer -n localhost:1025
---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/plain; charset="us-ascii"'
b'MIME-Version: 1.0'
b'Content-Transfer-Encoding: 7bit'
b'Subject: Test mail'
b'From: admin@example.com'
b'To: info@example.com'
b'X-Peer: ::1'
b''
b'This is test mail'
------------ END MESSAGE ------------
````


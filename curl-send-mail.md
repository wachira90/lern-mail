# curl send mail

````
curl --ssl smtp://mail.example.com --mail-from myself@example.com \
     --mail-rcpt receiver@example.com --upload-file email.txt \
     --user 'user@your-account.com:your-account-password'


curl --ssl-reqd smtp://mail.example.com --mail-from myself@example.com \
     --mail-rcpt receiver@example.com --upload-file email.txt \
     --user 'user@your-account.com:your-account-password'
````     

````

--ssl           Try SSL/TLS (FTP, IMAP, POP3, SMTP)
--ssl-reqd      Require SSL/TLS (FTP, IMAP, POP3, SMTP)

````

````
curl --ssl-reqd \
  --url 'smtps://smtp.gmail.com:465' \
  --user 'username@gmail.com:password' \
  --mail-from 'username@gmail.com' \
  --mail-rcpt 'john@example.com' \
  --upload-file mail.txt


mail.txt  => file content


From: "User Name" <username@gmail.com>
To: "John Smith" <john@example.com>
Subject: This is a test

Hi John,
I’m sending this mail with curl thru my gmail account.
Bye!
````

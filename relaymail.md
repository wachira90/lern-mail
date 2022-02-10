# Relaymail

## Install package
````
apt-get update && apt-get upgrade
sudo apt-get install libsasl2-modules
````
 
## Install postfix

SELECT => internet site => mail.example.com 

````
sudo apt-get install postfix
````
 
 
## file /etc/postfix/main.cf
````
myhostname = fqdn.example.com
````
 
 
## file /etc/postfix/sasl_passwd
````
[mail.isp.example] username@example.com:password
sudo postmap /etc/postfix/sasl_passwd
````
 
 
 ## Secure your Password and Hash DB files
````
 sudo chown root:root /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
 sudo chmod 0600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
````
 
 # Configuring the Relay Server
 
 ## file /etc/postfix/main.cf
````
 # specify SMTP relay host
relayhost = [mail.isp.example]:587
````
 
 
 ## file /etc/postfix/main.cf
 
````
 # enable SASL authentication
smtp_sasl_auth_enable = yes
# disallow methods that allow anonymous authentication.
smtp_sasl_security_options = noanonymous
# where to find sasl_passwd
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
# Enable STARTTLS encryption
smtp_use_tls = yes
# where to find CA certificates
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
````
 
 
 ##  restart service
 
````
sudo service postfix restart
````
 
 # Testing Your Postfix Configuration
 
 ## install package
````
sudo apt-get install mailutils
````
 
 
 ## test
````
echo  "body of your email" | mail -s "This is a subject" -a "From:you@example.com" recipient@elsewhere.com
````
 
 
## Note

You can use Postfix’s own Sendmail implementation to test your Postfix configuration. Replace the example’s values with your own. When you are done drafting your email type ctrl d.

````
sendmail recipient@elsewhere.com
From: you@example.com
Subject: Test mail
This is a test email
````
 
 
 

# lern-mail
How to send mail through Gmail On CentOS 7

## install package

yum -y install postfix cyrus-sasl-plain mailx

## nano /etc/postfix/main.cf

relayhost = [smtp.gmail.com]:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_tls_CAfile = /etc/ssl/certs/ca-bundle.crt
smtp_sasl_security_options = noanonymous
smtp_sasl_tls_security_options = noanonymous


##  nano /etc/postfix/sasl_passwd

[smtp.gmail.com]:587 username:password


## Create a Postfix lookup table from the sasl_passwd text file by running the following command.

postmap /etc/postfix/sasl_passwd


## Now Restrict access to the sasl_passwd files

chown root:postfix /etc/postfix/sasl_passwd

chmod 640 /etc/postfix/sasl_passwd


## Reload the Postfix configuration.

systemctl reload postfix

## test

echo "This is Manas." | mail -s "message" xxxxx@yyy.com

## tail -f /var/log/maillog

debug_peer_list=smtp.gmail.com

debug_peer_level=3


## Check Postfix Config:

[root@hostname ~]# postconf -n


systemctl status postfix

systemctl restart postfix

systemctl enable postfix

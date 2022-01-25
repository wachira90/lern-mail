# 3 Reject Email if SMTP Client Hostname doesn’t have valid A Record

A legitimate email server should also have a valid A record for its hostname. The IP address returned from A record should match the IP address of email server. To filter out emails from hosts that don’t have valid A record, edit Postfix main configuration file.

````
sudo nano /etc/postfix/main.cf
````
Add the following two lines in `smtpd_sender_restrictions.`
````
reject_unknown_reverse_client_hostname
reject_unknown_client_hostname
````
Example:
````
smtpd_sender_restrictions =
   permit_mynetworks
   permit_sasl_authenticated
   reject_unknown_reverse_client_hostname
   reject_unknown_client_hostname
````
Save and close the file. Then restart Postfix for the change to take effect.
````
sudo systemctl restart postfix
````

Note that `reject_unknown_client_hostname` does not require HELO from SMTP client. It will fetch the hostname from PTR record, then check the A record.

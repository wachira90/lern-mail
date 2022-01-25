# Reject Email If MAIL FROM Domain Has Neither MX Record Nor A Record

The `MAIL FROM` address is also known as `envelope from` address. Some spammers use a non-existent domain in the `MAIL FROM` address. If a domain name has no MX record, Postfix will find the A record of the main domain and send email to that host. If the sender domain has neither MX record nor A record, Postfix can’t send email to that domain. So why not reject emails that you can’t reply to?


To filter out this kind of spam, edit Postfix main configuration file.

````
sudo nano /etc/postfix/main.cf
````
Add the following line in `smtpd_sender_restrictions.` It will reject email if the domain name of the address supplied with the MAIL FROM command has neither MX record nor A record.
````
reject_unknown_sender_domain
````
Example:

````
smtpd_sender_restrictions =
   permit_mynetworks
   permit_sasl_authenticated
   reject_unknown_sender_domain
   reject_unknown_reverse_client_hostname
   reject_unknown_client_hostname
````
Save and close the file. Then restart Postfix for the change to take effect.

````
sudo systemctl restart postfix
````
Note that I placed this restriction above other `reject` restrictions. From my experience, if it is below other `reject` restrictions, it won’t work. (Maybe this only happens on my email server.)



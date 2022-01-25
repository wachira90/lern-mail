# 2 Enable HELO/EHLO Hostname Restrictions in Postfix

Some spammers don’t provide a valid HELO/EHLO hostname in the SMTP dialog. They can be non-fully qualified domain name, or a domain name doesn’t exist or only for an internal network. For example, a spammer using an Amazon EC2 instance to send spam is logged on my server as follows:


````
Aug 16 04:21:13 email postfix/smtpd[7070]: connect from ec2-54-237-201-103.compute-1.amazonaws.com[54.237.201.103]
Aug 16 04:21:13 email policyd-spf[7074]: prepend Received-SPF: None (mailfrom) identity=mailfrom; client-ip=54.237.201.103; helo=ip-172-30-0-149.ec2.internal; envelope-from=superdiem@carpaythe.tk; receiver=<UNKNOWN>
````
As you can see, the HELO hostname is ip-172-30-0-149.ec2.internal , which is only valid in AWS internal network. It has no valid A record nor MX record.

To enable HELO/EHLO hostname restriction, edit Postfix main configuration file.

````
sudo nano /etc/postfix/main.cf
````
First, add the following line to require the client to provide a HELO/EHLO hostname.
````
smtpd_helo_required = yes
````
Then add the following 3 lines to enable `smtpd_helo_restrictions.`
````
smtpd_helo_restrictions = 
    permit_mynetworks
    permit_sasl_authenticated
````
Use the following line to reject clients who provide malformed HELO/EHLO hostname.

````
reject_invalid_helo_hostname
````
Use the following line to reject non-fully qualified HELO/EHLO hostname.
````
reject_non_fqdn_helo_hostname
````
To reject email when the HELO/EHLO hostname has neither DNS A record nor MX record, use

````
reject_unknown_helo_hostname
````
Like this:

````
smtpd_helo_required = yes
smtpd_helo_restrictions =
    permit_mynetworks
    permit_sasl_authenticated
    reject_invalid_helo_hostname
    reject_non_fqdn_helo_hostname
    reject_unknown_helo_hostname
````
Save and close the file. Then reload Postfix.

````
sudo systemctl reload postfix
````
Note that although most legitimate mail servers have valid A record for the HELO/EHLO hostname, occasionally a legitimate mail server doesn’t meet this requirement. You need to whitelist them with `check_helo_access.`

````
smtpd_helo_required = yes
smtpd_helo_restrictions =
    permit_mynetworks
    permit_sasl_authenticated
    check_helo_access hash:/etc/postfix/helo_access
    reject_invalid_helo_hostname
    reject_non_fqdn_helo_hostname
    reject_unknown_helo_hostname
````
Then you need to create the `/etc/postfix/helo_access` file.

````
sudo nano /etc/postfix/helo_access
````
Whitelist legitimate mail server’s HELO/EHLO hostname like below.
````
optimus-webapi-prod-2.localdomain      OK
va-massmail-02.rakutenmarketing.com    OK
````
It’s likely that you don’t know which hostnames to whitelist, then simply copy the above two lines, which is the only lines in my `helo_access` file. You can always add more hostnames later. Save and close the file. Then run the following command to create the `/etc/postfix/helo_access.db` file.
````
sudo postmap /etc/postfix/helo_access
````
And reload Postfix.
````
sudo systemctl reload postfix
````

Finish.



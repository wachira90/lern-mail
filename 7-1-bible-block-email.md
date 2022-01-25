# 7 bible block email

In this tutorial, I’d like to share with you my 7 tips for blocking email spam with Postfix SMTP server. Over the last four years of running my own email server, I received lots of spam, aka unsolicited commercial email, most of which came from China and Russia. Spam exists because it’s so cheap to send a large volume of emails on the Internet. Postfix allows you to block spam before they get into your mailbox, so you can save bandwidth and disk space. This post is the result of my experience in fighting spam.

Note: If you plan to run your own mail server, I recommend using iRedmail, which really simplifies the process of setting up a mail server. It also ships with anti-spam rules. If you prefer to set up a mail server from scratch, then check out my mail server tutorial series.


## Characteristics of Spam

Below is what I found about email spam. These spam are easy to block.

- Their IP addresses don’t have PTR records.
- The spammer doesn’t provide valid hostname in HELO/EHLO clause.
- They spoof MAIL FROM address.
- They generally don’t re-send email after a failed email delivery.

Legitimate email servers should never have these characteristics. So here comes my 7 tips, which will block 90% of spam.

Fact: Around 93%~95% of emails in the world are rejected at the SMTP gateway, never landed in the inbox or spam folder.


## 1 Reject Email if SMTP Client Has no PTR record

PTR record maps an IP address to a domain name. It’s the counterpart to A record. On Linux, you can query the domain name associated with an IP address by executing the following command:
````
host <IP address>
````
For example, the following command returns the hostname of Google’s mail server.
````
host 209.85.217.172
````
Output:
````
172.217.85.209.in-addr.arpa domain name pointer mail-ua0-f172.google.com.
````
Due to the prevalence of spam, many mail servers (such as Gmail, gmx.com, gmx.net, facebook.com) require that SMTP clients have valid PTR records associated with their IP addresses. Every mail server admin should set PTR record for their SMTP servers. If the SMTP client has a PTR record, you can find a line in Postfix log like below.
````
connect from mail-ua0-f172.google.com[209.85.217.172]
````
If the SMTP client doesn’t have a PTR record, then the hostname will be identified as unknown.
````
connect from unknown[120.41.196.220]
````
To filter out emails with no PTR records, open Postfix main configuration file.
````
sudo nano /etc/postfix/main.cf
````
Add the following line in `smtpd_sender_restrictions`. This directive rejects an email if the client IP address has no PTR record.
````
reject_unknown_reverse_client_hostname
````
Example:
````
smtpd_sender_restrictions =
   permit_mynetworks
   permit_sasl_authenticated
   reject_unknown_reverse_client_hostname
   ````
Save and close the file. Then restart Postfix for the change to take effect.
````
sudo systemctl restart postfix
````

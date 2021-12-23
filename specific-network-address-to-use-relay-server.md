# Allow specific network address to use relay server

Similarly we can modify `mynetworks` value to allow all the network subnets to use our relay server for sending mails.

````
mynetworks = 192.168.43.0/24, 127.0.0.0/8
````

Now we allow all the IP Address in `192.168.43.0/24` subnet to be able to use our relay server for sending mails.

Reload the postfix service to activate our changes

````
# systemctl reload postfix
````

Now let's verify this configuration by sending mail from our `client-1.example.com`

````
Aug 01 13:14:21 client-1.example.com sendmail[10202]: 0717iL9A010202: to=root@mail.example.com, ctladdr=root (0/0), delay=00:00:00, xdelay=00:00:00, mailer=relay, pri=30231, relay=[127.0.0.1] [127.0.0.1], dsn=2.0.0, stat=Sent (Ok: queued as 1E91F5FDDE)
Aug 01 13:14:21 client-1.example.com postfix/smtpd[10203]: disconnect from localhost[127.0.0.1] ehlo=2 starttls=1 mail=1 rcpt=1 data=1 quit=1 commands=7
Aug 01 13:14:21 client-1.example.com postfix/smtp[10207]: 1E91F5FDDE: to=<root@mail.example.com>, relay=mail.example.com[192.168.43.154]:25, delay=0.21, delays=0.06/0.04/0.08/0.03, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 4B8745FCE3)
````

So this time the relay server allowed us to send mail from the client in `192.168.43.0/24` subnet


### Conclusion

In this tutorial we learned to allow or blacklist specified range of IP address or networks to allow or blacklist from using our postfix relay server. You can modify mynetworks value or use mynetworks_style to define your network. We may also choose to defer the mails instead of reject so that the mail goes to queue and will be sent later.

Lastly I hope the steps from the article to restrict access for postfix smtp relay server for certain IP address or network on Linux was helpful. So, let me know your suggestions and feedback using the comment section.


# Blacklist single IP Address to access relay server

### ENVIRONMENT
````
Postfix relay server: 192.168.43.154 (mail.example.com)
Postfix Client-1: 192.168.43.48 (client-1.example.com)
Postfix Client-2: 192.168.43.148 (client-2.example.com)

````

We will use `smtpd_relay_restrictions` to restrict `client-1.example.com` from using this relay server

Make the following changes on the relay server in `/etc/postfix/main.cf`

````
mynetworks = !192.168.43.48, 192.168.43.0/24, 127.0.0.0/8
````

### hint

Notice that I have placed the IP to be blocked before giving `192.168.43.0/24` because postfix will perform lookup left to right so if `192.168.43.0/24` is placed before the blacklisted IP, the provided IP will match in `192.168.43.0/24` subnet and will allow the relay, hence our setting will not work.


#### Add the following (Or modify the existing value if already defined in main.cf)

````
smtpd_relay_restrictions = permit_mynetworks, reject
````

So here we are rejecting request from any other network other than what is defined in `mynetworks` and additionally in `mynetworks` I have blacklisted my client's IP address

#### Reload the postfix service

````
# systemctl reload postfix
````

#### Now we try to send mail from our client-1.example.com

````
# mail root@client-2.example.com
Subject: Test message
Check bounce
.
EOT
````

Logs on `client-1.example.com`

````
Aug 02 00:35:35 client-1.example.com postfix/smtp[926]: 970F25FDF4: to=<root@client-2.example.com>, relay=mail.example.com[192.168.43.154]:25, delay=0.44, delays=0.08/0/0.25/0.11, dsn=5.7.1, status=bounced (host mail.example.com[192.168.43.154] said: 554 5.7.1 <root@client-2.example.com>: Recipient address rejected: Access denied (in reply to RCPT TO command))
````


Logs on `client-2.example.com`
````
No logs on client-2.example.com as the mail didn't reached here
````

Logs on `mail.example.com`
````
Aug 02 11:13:10 mail.example.com postfix/smtpd[21642]: NOQUEUE: reject: RCPT from client-1[192.168.43.48]: 554 5.7.1 <root@client-2.example.com>: Recipient address rejected: Access denied; from=<root@client-1.example.com> to=<root@client-2.example.com> proto=ESMTP helo=<client-1.example.com>
````

So our configuration to blacklist single IP Address from using SMTP relay server is working as expected.

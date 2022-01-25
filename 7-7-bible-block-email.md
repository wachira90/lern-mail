# 7 Set Up OpenDMARC to Reject Emails That Fail DMARC Check

DMARC (Domain-based Message Authentication, Reporting and Conformance) is an Internet standard that allows domain owners to prevent their domain names from being used by email spoofers. Please read one of the following guide to set up OpenDMARC.

https://www.linuxbabe.com/mail-server/opendmarc-postfix-ubuntu

https://www.linuxbabe.com/redhat/opendmarc-postfix-centos-rhel

## Don’t be an Open Relay

Mail servers that forward mail on behalf of anyone towards any destination is called open relay. In the beginning, this is a good thing. As time went by, open relays are abused by spammers and now open relays are often blacklisted. The following line in `/etc/postfix/main.cf` file prevents your email server from being an open relay.

````
smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated defer_unauth_destination
````
This line tells Postfix to forward email only from clients in trusted networks, from clients that have authenticated with SASL, or to domains that are configured as authorized relay destinations. It should be already in the main configuration file after you install Postfix.


## How to Stop SMTP AUTH Flood from Spammers

After some time, the spammer knew that he cannot get through my spam filter. This bad actor started flooding my email server with SMTP AUTH connections. In my `/var/log/mail.log` file, I can find the following messages.

````
Dec 14 09:58:37 email postfix/smtpd[22095]: connect from unknown[117.86.35.119]
Dec 14 09:58:37 email postfix/smtpd[22119]: lost connection after AUTH from unknown[114.232.141.99]
Dec 14 09:58:37 email postfix/smtpd[22119]: disconnect from unknown[114.232.141.99] ehlo=1 auth=0/1 commands=1/2
Dec 14 09:58:37 email postfix/smtpd[22119]: connect from unknown[180.120.191.91]
Dec 14 09:58:38 email postfix/smtpd[22095]: lost connection after AUTH from unknown[117.86.35.119]
Dec 14 09:58:38 email postfix/smtpd[22095]: disconnect from unknown[117.86.35.119] ehlo=1 auth=0/1 commands=1/2
Dec 14 09:58:38 email postfix/smtpd[22119]: lost connection after AUTH from unknown[180.120.191.91]
Dec 14 09:58:38 email postfix/smtpd[22119]: disconnect from unknown[180.120.191.91] ehlo=1 auth=0/1 commands=1/2
Dec 14 09:58:38 email postfix/smtpd[22095]: connect from unknown[49.67.68.34]
Dec 14 09:58:39 email postfix/smtpd[22106]: lost connection after AUTH from unknown[180.120.192.199]
Dec 14 09:58:39 email postfix/smtpd[22106]: disconnect from unknown[180.120.192.199] ehlo=1 auth=0/1 commands=1/2
Dec 14 09:58:39 email postfix/smtpd[22095]: lost connection after AUTH from unknown[49.67.68.34]
Dec 14 09:58:39 email postfix/smtpd[22095]: disconnect from unknown[49.67.68.34] ehlo=1 auth=0/1 commands=1/2
Dec 14 09:58:39 email postfix/smtpd[22119]: connect from unknown[121.226.62.16]
Dec 14 09:58:39 email postfix/smtpd[22119]: lost connection after AUTH from unknown[121.226.62.16]
Dec 14 09:58:39 email postfix/smtpd[22119]: disconnect from unknown[121.226.62.16] ehlo=1 auth=0/1 commands=1/2
Dec 14 09:58:39 email postfix/smtpd[22106]: connect from unknown[58.221.55.21]
Dec 14 09:58:40 email postfix/smtpd[22106]: lost connection after AUTH from unknown[58.221.55.21]
Dec 14 09:58:40 email postfix/smtpd[22106]: disconnect from unknown[58.221.55.21] ehlo=1 auth=0/1 commands=1/2
Dec 14 09:58:47 email postfix/smtpd[22095]: connect from unknown[121.232.65.223]
Dec 14 09:58:47 email postfix/smtpd[22095]: lost connection after AUTH from unknown[121.232.65.223]
Dec 14 09:58:47 email postfix/smtpd[22095]: disconnect from unknown[121.232.65.223] ehlo=1 auth=0/1 commands=1/2
````
Postfix is designed to run even under stressful conditions. It uses a limited amount of memory, so such attacks are much less effective. However, I don’t want them to appear in my mail log and we should save smtpd processes for legitimiate SMTP clients, instead of wasting time dealing with spambots. To stop this kind of flood attack, you can use fail2ban, which is a set of server and client programs to limit brute force authentication attempts. Install fail2ban from default Ubuntu repository.

````
sudo apt install fail2ban
````
After it’s installed, it will be automatically started, as can be seen with:

````
sudo systemctl status fail2ban
````
The `fail2ban-server` program included in fail2ban monitors log files and issues ban/unban command. By default, it would ban a client’s IP address for 10 minutes if the client failed authentication 5 times. The ban is done by adding iptables firewall rules. You can check iptables rules by running the following command.

````
sudo iptables -L
````
To enable fail2ban on Postifx SMTP AUTH attack, add the following lines in `/etc/fail2ban/jail.local` file. If the file doesn’t exist, then create this file.

````
[postfix-flood-attack]
enabled  = true
bantime  = 10m
filter   = postfix-flood-attack
action   = iptables-multiport[name=postfix, port="http,https,smtp,submission,pop3,pop3s,imap,imaps,sieve", protocol=tcp]
logpath  = /var/log/mail.log

````
You can change the bantime to something like `30m` or `12h` to ban the bad actor for longer time. If you would like to whitelist your own IP address, add the following line to tell fail2ban to ignore your IP address. Replace 12.34.56.78 with your own IP address. Multiple IP addresses are separated by spaces.

````
ignoreip = 127.0.0.1/8 ::1 12.34.56.78
````
By default, the allowed max number of failure it 5 times. After 5 failures, the client will be banned. To specify a customized number of failures, add the following line. Change the number to your liking.

````
maxretry = 4
````
Save and close the file. Then create the filter rule file.

````
sudo nano /etc/fail2ban/filter.d/postfix-flood-attack.conf
````
In this file, we specify that if the “lost connection after AUTH from” is found, then ban that IP address.

````
[Definition]
failregex = lost connection after AUTH from (.*)\[<HOST>\]
ignoreregex =
````

Save and close the file. Restart fail2ban the changes to take effect.
````
sudo systemctl restart fail2ban
````
In the fail2ban log file (/var/log/fail2ban.log), I can find the message like below, which indicates the IP address 114.223.221.55 has been banned because it failed authentication 5 times.

````
2018-12-14 09:52:15,598 fail2ban.filter [21897]: INFO [postfix-flood-attack] Found 114.223.211.55 - 2018-12-14 09:52:15
2018-12-14 09:52:16,485 fail2ban.filter [21897]: INFO [postfix-flood-attack] Found 114.223.211.55 - 2018-12-14 09:52:16
2018-12-14 09:52:20,864 fail2ban.filter [21897]: INFO [postfix-flood-attack] Found 114.223.211.55 - 2018-12-14 09:52:20
2018-12-14 09:52:21,601 fail2ban.filter [21897]: INFO [postfix-flood-attack] Found 114.223.211.55 - 2018-12-14 09:52:21
2018-12-14 09:52:22,102 fail2ban.filter [21897]: INFO [postfix-flood-attack] Found 114.223.211.55 - 2018-12-14 09:52:22
2018-12-14 09:52:22,544 fail2ban.actions [21897]: NOTICE [postfix-flood-attack] Ban 114.223.211.55
````
I can also check my iptables.

````
sudo iptables -L
````
Output:

````
Chain f2b-postfix (1 references)
target     prot opt source               destination         
REJECT     all  --  195.140.231.114.broad.nt.js.dynamic.163data.com.cn  anywhere             reject-with icmp-port-unreachable
RETURN     all  --  anywhere             anywhere
````
This indicates fail2ban has set up a iptables rule that reject connection from `195.140.231.114.broad.nt.js.dynamic.163data.com.cn,` which is a hostname is used by the spammer.

If you would like to manually block an IP address, run the following command. Replace 12.34.56.78 with the IP address you want to block.

````
sudo iptables -I INPUT -s 12.34.56.78 -j DROP
````
If you use UFW (iptables frontend), then run

````
sudo ufw insert 1 deny from 12.34.56.78 to any
````

## How To Stop Repeat Senders Who Failed Postfix Check

Some spammers use automated tools to send spam. They ignore the Postfix reject message and continue sending spam. For example, sometimes I can see the following message in Postfix summary report.

````
504 5.5.2 : Helo command rejected: need fully-qualified hostname; from=<123123@linuxbabe.com> to=<martinlujan997@gmail.com> proto=ESMTP helo= (total: 1)
           1   185.191.228.36
 504 5.5.2 : Helo command rejected: need fully-qualified hostname; from=<123456@linuxbabe.com> to=<martinlujan997@gmail.com> proto=ESMTP helo= (total: 1)
           1   185.191.228.36
 504 5.5.2 : Helo command rejected: need fully-qualified hostname; from=<3vrgfqblaepzfoieznbfntmrpqyix@linuxbabe.com> to=<martinlujan997@gmail.com> proto=ESMTP helo= (total: 1)
           1   185.191.228.36
 504 5.5.2 : Helo command rejected: need fully-qualified hostname; from=<6khdgqr6j@linuxbabe.com> to=<martinlujan997@gmail.com> proto=ESMTP helo= (total: 1)
           1   185.191.228.36
 504 5.5.2 : Helo command rejected: need fully-qualified hostname; from=<a1b2c3d4@linuxbabe.com> to=<martinlujan997@gmail.com> proto=ESMTP helo= (total: 1)
           1   185.191.228.36
 504 5.5.2 : Helo command rejected: need fully-qualified hostname; from=<abuse@linuxbabe.com> to=<martinlujan997@gmail.com> proto=ESMTP helo= (total: 1)
````
This spammer continues sending spam, ignoring the Postfix reject message: `Helo command rejected: need fully-qualified hostname.` To stop this kind of behavior, we can also use Fail2ban by adding the following lines in `/etc/fail2ban/jail.local` file.

````
[postfix]
enabled = true
maxretry = 3
bantime = 1h
filter = postfix
logpath = /var/log/mail.log
````

The `[postfix]` jail will use the builtin filter shipped with Fail2ban (/etc/fail2ban/filter.d/postfix.conf). Save and close the file. Then restart Fail2ban.



````
sudo systemctl restart fail2ban
````

Now the spammer will have to wait 1 hour before pounding your mail server again.

## Bonus Tip For iRedMail Users

iRedMail automatically configures Postscreen with Postfix. By default, there is a pregreet test in Postscreen to detect spam. As you may already know, in SMTP protocol, the receiving SMTP server should always declare its hostname before the sending SMTP server does so. Some spammers violate this rule and declare their hostnames before the receiving SMTP server does.

Sometimes I can see the following lines in `/var/log/mail.log` file, which indicates that this sender declare its hostname first. This spammer just want to pound my mail server with endless connections, but has no intent to send any email. And the EHLO hostname `ylmf-pc` is a clear indication that these connections are originated from compromised home computers. (`ylmf` is an acronym for the defunct Chinese Linux distro: `雨林木风.`)


````
PREGREET 14 after 0.22 from [121.226.63.86]:64689: EHLO ylmf-pc\r\n
PREGREET 14 after 0.24 from [121.232.8.131]:55705: EHLO ylmf-pc\r\n
PREGREET 14 after 0.24 from [114.232.9.57]:62783: EHLO ylmf-pc\r\n
````


iRedMail ships with a fail2ban rule to filter this kind of malicious activities. You can see the following line in `/etc/fail2ban/filter.d/postfix.iredmail.conf` file.


````
PREGREET .* from \[<HOST>\]:.* EHLO ylmf-pc
````
But I think the default bantime (1 hour) for this filter to too low. Open the /etc/fail2ban/jail.local file and add a custom bantime parameter like below.


````
[postfix-iredmail]
enabled   =  true
max-retry =  1
bantime   =  24h
filter    =  postfix.iredmail
logpath   =  /var/log/mail.log
````

I set the bantime value to 24 hours because the sender is clearly using compromised home computers. Save and close the file. Restart fail2ban the changes to take effect.



````
sudo systemctl restart fail2ban
````

## Running Local DNS Resolver to Speed Up DNS Lookups

As you can see, Postfix will need to lookup DNS records in order to analyze each SMTP dialog. To speed up DNS lookups, you can run a local DNS resolver by following on the tutorials below.

- Run Your Own BIND DNS Resolver on Debian https://www.linuxbabe.com/debian/dns-resolver-debian-10-buster-bind9
- Run Your Own BIND DNS Resolver on Ubuntu 18.04 https://www.linuxbabe.com/ubuntu/set-up-local-dns-resolver-ubuntu-18-04-16-04-bind9
- Run Your Own BIND DNS Resolver on Ubuntu 20.04 https://www.linuxbabe.com/ubuntu/set-up-local-dns-resolver-ubuntu-20-04-bind9
- Run Your Own BIND DNS Resolver on CentOS/RHEL  https://www.linuxbabe.com/redhat/bind-9-dns-resolver-centos-8

And most DNS blacklists have query limit. Running your own local DNS resolver to cache DNS records can help you stay under the query limit.







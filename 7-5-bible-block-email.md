# 5 Enable Greylisting in Postfix

As required by the SMTP protocol, any legitimate SMTP client must be able to re-send email if delivery fails. (By default, Postfix is configured to resend failed emails many times before it informs the sender that the message could not be delivered.) Many spammers usually just send once and would not retry.

`Postgrey` is a greylisting policy server for Postfix. Debian and Ubuntu users can install `postgrey` from the default repository.

````
sudo apt install postgrey
````
CentOS/RHEL users can install it from EPEL repository.
````
sudo dnf install epel-release
sudo dnf install postgrey
````
Once it’s installed, start it with systemctl.
````
sudo systemctl start postgrey
````
Enable auto-start at boot time.
````
sudo systemctl enable postgrey
````
On Debian and Ubuntu, it listens on TCP port 10023 on localhost (both IPv4 and IPv6).
````
sudo netstat -lnpt | grep postgrey
````
On CentOS/RHEL, Postgrey listens on a Unix socket (`/var/spool/postfix/postgrey/socket`).

Next, we need to edit Postfix main configuration file to make it use the greylisting policy server.
````
sudo nano /etc/postfix/main.cf
````
Add the following line in smtpd_recipient_restrictionsif you are using Debian or Ubuntu.
````
check_policy_service inet:127.0.0.1:10023
````
If you use CentOS/RHEL, you need to add the following line instead.
````
check_policy_service  unix:/var/spool/postfix/postgrey/socket
````
In case you don’t know, the directive check_policy_service unix:private/policyd-spf in the above screenshot will make Postfix check SPF record on the sender’s domain. This directive requires you to install and configure the postfix-policyd-spf-python package.

Save and close the file. Then restart Postfix.
````
sudo systemctl restart postfix
````
From now on, Postgrey will reject an email if the sender triplet (sender IP address, sender email address, recipient email address) is new. The following log message in `/var/log/mail.log` shows a new sender triplet. The action `greylist` means this email message was rejected.
````
postgrey[1016]: action=greylist, reason=new, client_name=unknown, client_address=117.90.24.148/32, sender=pnccepjeu@rhknqj.net, recipient=xiao@linuxbabe.com
````
From my experience, Chinese email spammers like to use a fake, weird-looking and randomly generated sender address for every email, so adding these fake email addresses to blacklist won’t stop them. On the other hand, they never try re-sending a rejected email with the same sender address, which means greylisting can be very effective at stopping this kind of spam.


## Fixing Error on Debian & Ubuntu

If you see the following error in mail log (/var/log/mail.log)
````
warning: connect to 127.0.0.1:10023: Connection refused
warning: problem talking to server 127.0.0.1:10023: Connection refused
````
The problem is that postgrey is not running. You need to specify 127.0.0.1 as the listening address in  /etc/default/postgrey file. So change the following line
````
POSTGREY_OPTS="--inet=10023"
````
to
````
POSTGREY_OPTS="--inet=127.0.0.1:10023"
````
Then restart postgrey.
````
sudo systemctl restart postgrey
````
Check if it’s listening:
````
sudo netstat -lnpt | grep 10023
````


## How to Minimize Bad User Experience

Greylisting can result in bad experience for the end user, as the user has to wait another several minute for the email to arrive. To minimize this bad experience, you can create a whitelist, and use a second MX record that points to the same host.

### Whitelist

Postgrey ships with two whitelist files (`/etc/postgrey/whitelist_clients` and `/etc/postgrey/whitelist_recipients`). The former contains a list of hostnames and the latter contains a list of recipient addresses.

By default, Google’s mail servers are whitelisted. No matter the sender is using a @gmail.com address or other address, as long as the sender is using Google’s mail server, Postgrey won’t reject the email. The following line in my `/var/log/mail.log` file shows this.

````
postgrey[1032]: action=pass, reason=client whitelist, client_name=mail-yb0-f190.google.com
````
Note: You can also see postgrey logs with this command `sudo journalctl -u postgrey.`

You can add other hostnames in `/etc/postgrey/whitelist_clients` file, like

````
facebook.com
bounce.twitter.com
blogger.com
email.medium.com
````
You can get these hostnames with a tool called `pflogsumm` which I will discuss later in this article. Save and close the file, the restart Postgrey.
````
sudo systemctl restart postgrey
````

## Create Another MX Hostname with the Same IP Address

You can specify more than one MX record for your domain name like below.

````
Record Type    Name      Mail Server            Priority

MX             @         mail.yourdomain.com     0
MX             @         mail2.yourdomain.com    5
````
The sender will try the first mail server (with priority 0). If mail.yourdomain.com rejects email by greylisting, then the sender would immediately try the second mail server (with priority 5).

If the two mail server hostnames have the same IP address, then when the sender tries the second mail server hostname, the email will be accepted immediately (if all other checks pass) and end users will not notice email delay caused by greylisting.

Note that this requires you to set a very small delay time like 1 second in `/etc/default/postgrey` (Debian & Ubuntu) or `/etc/sysconfig/postgrey` (CentOS/RHEL). The delay time tells the SMTP client how many seconds to wait before sending again. If the delay time is not small enough, then the second email delivery would still be rejected.


Debian/Ubuntu

````
POSTGREY_OPTS="--inet=127.0.0.1:10023 --delay=1"
````

CentOS/RHEL

````
POSTGREY_DELAY="--delay=1"
````

Restart Postgrey.

````
sudo systemctl restart postgrey
````

Also beware that not all mail servers would immediately try the second MX host.








# 6 Using Public Realtime Blacklists


There are spam emails that are sent from servers that has a valid hostname, valid PTR record and can pass through grey listing. In this case, you can use blacklisting to reject spam. There are many public realtime blacklists (RBL), also known as DNSBLs (DNS based lists). By realtime it means that the list is always changing. An IP address or domain name could be on the list today and off the list tomorrow, so you could get different result depending on when you query the list.

You can use multiple blacklists to block spam. Go to https://www.debouncer.com and mxtoolbox.com , enter the spammer’s domain and IP address to see which blacklists are blocking them, then you can use those blacklists. For example, I found that spammers are blacklisted by one of the following blacklists:


- dbl.spamhaus.org
- zen.spamhaus.org
- multi.uribl.com
- ivmURI
- InvaluementURI

So I can add the following configurations in `/etc/postfix/main.cf` file. Some public blacklisting service requires monthly fee. For now, I’m using the free service of spamhaus.org.


````
smtpd_recipient_restrictions =
   permit_mynetworks,
   permit_sasl_authenticated,
   check_policy_service unix:private/policyd-spf,
   check_policy_service inet:127.0.0.1:10023,
   reject_rhsbl_helo dbl.spamhaus.org,
   reject_rhsbl_reverse_client dbl.spamhaus.org,
   reject_rhsbl_sender dbl.spamhaus.org,
   reject_rbl_client zen.spamhaus.org
````
Where:

- `rhs` stands for right hand side, i.e, the domain name.
- `reject_rhsbl_helo` makes Postfix reject email when the client HELO or EHLO hostname is blacklisted.
- `reject_rhsbl_reverse_client:` reject the email when the unverified reverse client hostname is blacklisted. Postfix will fetch the client hostname from PTR record. If the hostname is blacklisted, reject the email.
- `reject_rhsbl_sender` makes Postfix reject email when the MAIL FROM domain is blacklisted.
- `reject_rbl_client:` This is an IP-based blacklist. When the client IP address is backlisted, reject the email.

Some spammers use Google’s mail server, so `reject_rhsbl_helo` is ineffective, but most of them use their own domain names in the MAIL FROM header, so `reject_rhsbl_sender` will be effective.

## Create A Whitelist

Sometimes there are legitimate email servers blacklisted. You can create a whitelist so they won’t be blocked. Create the following file.

````
sudo nano /etc/postfix/rbl_override
````
In this file, whitelist domain names like below.

````
dripemail2.com  OK           //This domain belongs to drip.com

mlsend.com      OK           //This domain belongs to mailerlite email marketing service
````
Save and close the file. Then run the following command to create the `rbl_override.db` file.
````
sudo postmap /etc/postfix/rbl_override
````
Edit Postfix main configuration file.

````
sudo nano /etc/postfix/main.cf
````
In `smtpd_recipient_restrictions` add the following line.

````
check_client_access hash:/etc/postfix/rbl_override,
````
Like below. It should be place above other RBL checks.
````
smtpd_recipient_restrictions =
   permit_mynetworks,
   permit_sasl_authenticated,
   check_policy_service unix:private/policyd-spf,
   check_policy_service inet:127.0.0.1:10023,
   check_client_access hash:/etc/postfix/rbl_override,
   reject_rhsbl_helo dbl.spamhaus.org,
   reject_rhsbl_reverse_client dbl.spamhaus.org,
   reject_rhsbl_sender dbl.spamhaus.org,
   reject_rbl_client zen.spamhaus.org
````

Reload Postfix for the changes to take effect.

````
sudo systemctl reload postfix
````

## Using Public Whitelist to Reduce False Positive


Maintaining a private whitelist is necessary sometimes, but you can also use public whitelists, the most famous of which is dnswl.org. Currently, there is only a whitelist for IP address. Domain name whitelist is in beta. To use it, put the following line in `smtpd_recipient_restrictions.`

````
permit_dnswl_client list.dnswl.org=127.0.[0..255].[1..3],
````

Like below. It should be placed above the `reject_rbl_client` check.


````
smtpd_recipient_restrictions =
   permit_mynetworks,
   permit_sasl_authenticated,
   check_policy_service unix:private/policyd-spf,
   check_policy_service inet:127.0.0.1:10023,
   check_client_access hash:/etc/postfix/rbl_override,
   reject_rhsbl_helo dbl.spamhaus.org,
   reject_rhsbl_reverse_client dbl.spamhaus.org,
   reject_rhsbl_sender dbl.spamhaus.org,
   permit_dnswl_client list.dnswl.org=127.0.[0..255].[1..3],
   reject_rbl_client zen.spamhaus.org
````

Another well-known whitelist is swl.spamhaus.org, so you can also add it to your configuration.
````
permit_dnswl_client swl.spamhaus.org,
````

It’s impossible for an IP address to be listed in Spamhaus whitelist and blacklist at the same time, so if you only use Spamhaus blacklist in Postfix, then it’s not necessary to check against Spamhaus whitelist.

## My Postfix Spam filters

Here’s a screenshot of my Postfix spam filters.

![img logo](/img/6-003.JPG "img")


You might be wondering why there is no comma in the first two configuration snippets. Well, you can separate values in Postfix configuration file with space, carriage return or comma. If you add comma to one parameter (`smptd_recipient_restrictions` as in the above screenshot), then make sure all remaining values are separated with comma.


## Postfix Log Report

`Pflogsumm` is a great tool to create a summary of Postfix logs. Install it on Ubuntu with:

````
sudo apt install pflogsumm
````

On CentOS/RHEL, pflogsumm is provided by the postfix-perl-scripts package.


````
sudo dnf install postfix-perl-scripts
````

Use the following command to generate a report for today. (Note that on CentOS/RHEL, the mail log file is `/var/log/maillog.`)


````
sudo pflogsumm -d today /var/log/mail.log
````

Generate a report for yesterday.


````
sudo pflogsumm -d yesterday /var/log/mail.log
````

If you like to generate a report for this week.


````
sudo pflogsumm /var/log/mail.log
````

To emit `problem` reports (bounces, defers, warnings, rejects) before “normal” stats, use `--problems-first` flag.


````
sudo pflogsumm -d today /var/log/mail.log --problems-first
````

To append the email from address to each listing in the reject report, use  `--rej-add-from ` flag.


````
sudo pflogsumm -d today /var/log/mail.log --rej-add-from
````
To show the full reason in reject summaries, use `--verbose-msg-detail` flag.

````
sudo pflogsumm -d today /var/log/mail.log --rej-add-from --verbose-msg-detail
````

You can add a cron job to make pflogsumm to send a report to your email address every day.

````
sudo crontab -e
````
Add the following line, which will generate a report every day at 4:00 AM.

````
0 4 * * * /usr/sbin/pflogsumm -d yesterday /var/log/mail.log --problems-first --rej-add-from --verbose-msg-detail -q
````

To receive the report via email, add the following line above all cron jobs.

````
MAILTO="your-email-address"
````

You should pay attention to the message reject detail section, where you can see for what reason those emails are rejected and if there’s any false positives. Greylisting rejections are safe to ignore.

![img logo](/img/6-004.JPG "img")

If the MAILTO variable has already been set but you want Postfix log summary sent to a different email address, you can put the following line in your Cron job.

````
0 4 * * * /usr/sbin/pflogsumm -d yesterday /var/log/mail.log --problems-first --rej-add-from --verbose-msg-detail -q | mutt -s "Postfix log summary"  your-email-address
````

The output of `pflogsumm` command is redirected to `mutt`, a command line mail user agent, which will use the output as the email body and send it to the email address you specify at the end. Of course, you need to install mutt on your Linux server.
````
sudo apt install mutt
````
or
````
sudo dnf install mutt
````

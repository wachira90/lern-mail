## SASL LOGIN authentication failed: UGFzc3dvcmQ6
````
Dec 17 19:55:57 mail postfix/smtpd[10346]: disconnect from _gateway[192.168.200.254] ehlo=1 mail=1 rcpt=1 data=0/1 quit=1 commands=4/5
Dec 17 19:56:18 mail postfix/smtps/smtpd[10063]: warning: _gateway[192.168.200.254]: SASL LOGIN authentication failed: UGFzc3dvcmQ6
Dec 17 19:56:23 mail postfix/smtps/smtpd[10063]: lost connection after AUTH from _gateway[192.168.200.254]
Dec 17 19:56:23 mail postfix/smtps/smtpd[10063]: disconnect from _gateway[192.168.200.254] ehlo=1 auth=0/1 rset=1 commands=2/3
````

## brute force message name Password:
````
[root@mail1 ~]$ echo "UGFzc3dvcmQ6" | base64 -d
Password:
````

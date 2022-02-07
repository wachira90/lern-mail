# Lerning mail server

## Check config postfix

````
postconf -n
````

## Check config dovecot

````
dovecot -n
````
## Remove particular mail queue id (on running mailq command,you will get mail queue id)
````
postsuper -d mail_queue_id
````

## Remove ALL mails from queue
````
postsuper -d ALL
````

## Remove only ALL deferred mails which are in queue
````
postsuper -d ALL deferred
````

## SMTP port
````
25
465 (ssl)
2525
587
````

## POP 
````
110
995 (ssl)
````

## IMAP
````
143
993 (ssl)
````

# header body check example

### header_checks =  regexp:/etc/postfix/header_checks
    
###  body_checks = regexp:/etc/postfix/body_checks

### /etc/postfix/header_checks:

````
/^Received: +from +(porcupine\.org) +  reject forged client name in Received: header: $1
/^Received: +from +[^ ]+ +\(([^ ]+ +[he]+lo=|[he]+lo +)(porcupine\.org)\)    reject forged client name in Received: header: $2
/^Message-ID:.*@(porcupine\.org)	reject forged domain name in Message-ID: header: $1
````
### /etc/postfix/body_checks:

````
/^[> ]*Received: +from +(porcupine\.org)  reject forged client name in Received: header: $1
/^[> ]*Received: +from +[^ ]+ +\(([^ ]+ +[he]+lo=|[he]+lo +)(porcupine\.org)\)  reject forged client name in Received: header: $2
/^[> ]*Message-ID:.*@(porcupine\.org)  reject forged domain name in Message-ID: header: $1
````
    

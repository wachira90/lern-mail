# allow send specific domain 

# method 1

## nano  /etc/postfix/main.cf

### add
````
transport_maps = hash:/etc/postfix/transport
````

### content  /etc/postfix/transport
````
.example.com   :
example.com    :
*              discard:
````


# method 2

## open /etc/postfix/access 
````
nano /etc/postfix/access
````

### contents
````
example.com    OK
````
OR
````
user1@example.com    OK
user2@example.com    OK
````
###  postmap command
````
postmap /etc/postfix/access
````

### add main.cf

````
smtpd_recipient_restrictions = 
    hash:/etc/postfix/access
    reject
````

### restart service

````
systemctl restart postfix
````

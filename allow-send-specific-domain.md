# allow send specific domain

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

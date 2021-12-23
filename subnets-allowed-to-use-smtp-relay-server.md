# Define subnets allowed to use smtp relay server

## In postfix we have two variables which controls this behaviour to permit relay
````
mynetworks_style
mynetworks
````
### mynetworks_style
The method to generate the default value for the mynetworks parameter. This is the list of trusted networks for relay access control etc.

Specify `mynetworks_style = host` when Postfix should `trust` only the local machine.

Specify `mynetworks_style = subnet` when Postfix should `trust` remote SMTP clients in the same IP subnetworks as the local machine.

Specify `mynetworks_style = class` when Postfix should `trust` remote SMTP clients in the same IP class A/B/C networks as the local machine.


### mynetworks

- The list of `trusted` remote SMTP clients that have more privileges than `strangers`

- In particular, `trusted` SMTP clients are allowed to relay mail through Postfix

- You can specify the list of `trusted` network addresses by hand or you can let Postfix do it for you (which is the default)

- If you specify the `mynetworks` list by hand, Postfix ignores the `mynetworks_style` setting.

- Specify a list of network addresses or network/netmask patterns, separated by commas and/or whitespace. Continue long lines by starting the next line with whitespace.

- The list is matched **left to right** , and the search stops on the first match.

- Specify `!pattern` to **exclude** an address or network block from the list.

#### For example:

````
mynetworks = 127.0.0.0/8 168.100.189.0/28
mynetworks = !192.168.0.1, 192.168.0.0/28
````

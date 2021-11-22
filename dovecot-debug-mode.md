FROM => https://docs.iredmail.org/debug.dovecot.html

dovecot.conf
````
mail_debug = yes
````
## If you need authentication and password related debug message, turn on related settings and restart dovecot service.
````
auth_verbose = yes
auth_debug = yes
auth_debug_passwords = yes

# Set to 'yes' or 'plain', to output plaintext password (NOT RECOMMENDED).
auth_verbose_passwords = plain
````

## If Dovecot service cannot start, please run it manually, it will print the error message on console:
````
dovecot -c /etc/dovecot/dovecot.conf

````
## Debug LDAP queries
````
nano /etc/dovecot/dovecot-ldap.conf

debug_level = 1
````

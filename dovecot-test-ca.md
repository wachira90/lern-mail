# Test CA

## Client certificate verification/authentication
## If you want to require clients to present a valid SSL certificate, you’ll need these settings:
````
ssl_ca = </etc/ssl/ca.pem
ssl_verify_client_cert = yes

auth_ssl_require_client_cert = yes
# if you want to get username from certificate as well, enable this
#auth_ssl_username_from_cert = yes
````

## This will make Dovecot log all the problems it sees with SSL connections. Some errors might be caused by dropped connections, so it could be quite noisy.
````
verbose_ssl = yes
````

## Test CA command
````
openssl s_client -servername mail.example.com -connect mail.example.com:pop3s
````

## Error sms  (not ok)
````
Verify return code: 19 (self signed certificate in certificate chain)
````

## Testing CA On Debian
````
openssl s_client -CApath /etc/ssl/certs -connect mail.example.com:pop3s
````
## Testing CA On RHEL
````
openssl s_client -CAfile /etc/pki/tls/cert.pem -connect mail.example.com:pop3s
````
## Testing CA Success (this ok)
````
Verify return code: 0 (ok)
````

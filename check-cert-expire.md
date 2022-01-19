# check cert *.crt expire

## command
````
root@mail:~# openssl x509 -enddate -noout -in /etc/ssl/certs/ca-certificates.crt
notAfter=Dec 31 09:37:37 2030 GMT
````

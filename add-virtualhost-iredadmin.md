# add virtualhost iredadmin

### environment 
````
exist => mail.example.com
add new => mail.examplexxx.com
````

## check A, MX  reccord corect  mail.examplexxx.com
````
mail.examplexxx.com
````

## add host in program iredadmin
````
mail.examplexxx.com
````

## generate SSL letencrypt (nginx)

````
apt-get install certbot python-certbot-nginx -y

certbot certonly --webroot -w /var/www/html -d mail.example.com -w /var/www/html -d mail.examplexxx.com
````

## add /etc/hosts
````
127.0.0.1 mail.example.com mail
127.0.0.1 mail.examplexxx.com mail   <= add new
150.123.45.67 mail.example.com mail
150.123.45.67 mail.examplexxx.com mail  <= add new
````

## Finish 

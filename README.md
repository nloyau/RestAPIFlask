# RestAPIFlask

A simple app for testing REST API on Flask with data encryption

## With SSL embed

### Generate ssl cert

 mkdir ssl
 echo "ssl/" >> .gitignore
 openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365

### add entry point info

 if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))

### run flask with this param

 flask run --cert=ssl/cert.pem --key=ssl/key.pem
# Flask-LDAP-Auth

Flask-LDAP is intended to be a simple Flask extension that allows you
to perform authentication against a LDAP server.

The code is quite straight-forward, and can be hacked to implement other auth techniques.


## Requirements

 * Flask
 * pyldap

## Installation

Of course, the preferred way is via pip

```
$ pip install flask-ldap-auth
```

## Usage

In you brand new Flask app (say `hello.py`), you can use flask-ldap like this:

```python

from flask_ldap_auth import login_required, token
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somethingsecret'
app.config['LDAP_AUTH_SERVER'] = 'ldap://your_ldap_server_address'
app.config['LDAP_TOP_DN'] = 'ou=people,dc=your_org,dc=your_domain'
app.register_blueprint(token, url_prefix='/auth')


@app.route('/')
@login_required
def hello():
    return 'Hello, world'


if __name__ == '__main__':
    app.run()
```

Then serve it:

```
$ python hello.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


```

Let's say you want to access the `/` endpoint. Using `httpie` you'll do:

```
$ http GET http://127.0.0.1:5000/
HTTP/1.0 401 UNAUTHORIZED
Content-Length: 93
Content-Type: text/html; charset=utf-8
Date: Thu, 16 Nov 2017 13:52:58 GMT
Location: http://127.0.0.1:5000/auth/request-token
Server: Werkzeug/0.12.2 Python/3.5.3
WWW-Authenticate: Basic realm="Authentication Required"

{
    "error": "unauthorized",
    "message": "Please authenticate with a valid token",
    "status": 401
}

```

See? It asks for a token, and points you to the right URL in order to get a valid one (see `Location` in the headers).

So to ask for a token, you must do:

```
$ http --auth your_username POST http://127.0.0.1:5000/auth/request-token
http: password for your_username@127.0.0.1:5000:
```

Type in your password (don't worry if nothing is displayed on-screen), and you'll received a shiny new token:

```
HTTP/1.0 200 OK
Content-Length: 189
Content-Type: application/json
Date: Thu, 16 Nov 2017 13:53:00 GMT
Server: Werkzeug/0.12.2 Python/3.5.3

{
    "token": "a_token:"
}
```

You can also specify the desired duration of the token (by default it's 3600 seconds) by passing the `token_duration` parameter to your request:

```
$ http --auth your_username POST http://127.0.0.1:5000/auth/request-token token_duration==3600
http: password for your_username@127.0.0.1:5000:
```

If you do not search username against the default `uid` parameter, you must pass `search_criteria=yourcriteria` to your url parameters

```
$ http --auth your_username POST http://127.0.0.1:5000/auth/request-token search_criteria==cn
http: password for your_username@127.0.0.1:5000:
```

If your LDAP server does not allow anonymous binding, you must tell the API by:

 - providing credentials in your Flask app configuration with the following parameters: `LDAP_USERNAME` and `LDAP_PASSWORD`
 - using `authenticated_search=true` in the url parameters

```
$ http --auth your_username POST http://127.0.0.1:5000/auth/request-token  authenticated_search==true
http: password for your_username@127.0.0.1:5000:
```


Now you can use this token and access the `/` endpoint:

```
$ TK='a_token:'
$ http --auth $TK GET http://127.0.0.1:5000/
HTTP/1.0 200 OK
Content-Length: 12
Content-Type: text/html; charset=utf-8
Date: Thu, 16 Nov 2017 13:53:10 GMT
Server: Werkzeug/0.12.2 Python/3.5.3

hello, world

```


## How it works

You may have noticed, in the above example, that we defined this:

```python
app.register_blueprint(token, url_prefix='/auth')
```

This means that, we provided the application  _flask_ldap.token_ under the uri `/auth` .


The fact is that `login_required` awaits a token for Basic HTTP Authentication. In other words, instead of passing (username, password) when authenticating you must pass (token,) .

That token is then verified (using the SECRET_KEY you've set in your app's config).

To obtain a token, you must pass (username, password) to the endpoint /auth/request-token. `username`and `password` are your actual LDAP credentials.

The obtained token is valid 1h.



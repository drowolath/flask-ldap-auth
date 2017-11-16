#!/usr/bin/env python
# encoding: utf-8


from functools import wraps
from flask import Blueprint, current_app, jsonify, Response, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
import json
import ldap


token = Blueprint('token', __name__)


def authenticate():
    message = {
        'error': 'unauthorized',
        'message': 'Please authenticate with a valid token',
        'status': 401
        }
    response = Response(
        json.dumps(message),
        401,
        {
            'WWW-Authenticate': 'Basic realm="Authentication Required"',
            'Location': url_for('token.request_token')
            }
        )
    return response


def auth_ldap_required(func):
    """LDAP authentication decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not User.verify_auth_token(auth.username):
            return authenticate()
        return func(*args, **kwargs)
    return wrapper


@token.route('/request-token', methods=['POST'])
def request_token():
    """Simple app to generate a token"""
    auth = request.authorization
    user = User(auth.username)
    print(auth.username)
    if not auth or not user.verify_password(auth.password):
        return authenticate()
    response = {
        'token': user.generate_auth_token() + ':'
        }
    return jsonify(response)

# EOF

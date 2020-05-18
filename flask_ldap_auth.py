#!/usr/bin/env python
# encoding: utf-8


from functools import wraps
from flask import Blueprint, current_app, jsonify, Response, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
import json
import ldap


token = Blueprint('token', __name__)


__all__ = [
    'login_required',
    'token'
    ]


class User(object):

    def __init__(self, username):
        self.username = username

    def verify_password(self, password, **kwargs):
        """Method to check if provided password is valid"""
        search_criteria = kwargs.get('search_criteria', 'uid')
        full_dn = (
            f'{search_criteria}={current_app.config["LDAP_USERNAME"]},'
            f'{current_app.config["LDAP_TOP_DN"]}'
            )
        connection = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
        if kwargs.get('authenticated_search', None):
            # authenticate to LDAP server before performing a search
            # need to provide in your Flask app's config parameters
            # to do so
            connection.bind_s(
                full_dn,
                current_app.config["LDAP_PASSWORD"],
                ldap.AUTH_SIMPLE
                )
        result = connection.search_s(
            current_app.config['LDAP_TOP_DN'],
            ldap.SCOPE_ONELEVEL,
            f'({search_criteria}={self.username})'
            )
        if not result:
            return False
        dn = result[0][0]
        try:
            connection.bind_s(dn, password)
        except ldap.INVALID_CREDENTIALS:
            return False
        else:
            connection.unbind_s()
            return True

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({'username': self.username}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired, TypeError):
            return None
        return User(data['username'])


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


def login_required(func):
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
    kwargs = {
        'authenticated_search': request.args.get('authenticated_search', False),
        'search_criteria': request.args.get('search_criteria')
        }
    if not auth or not user.verify_password(auth.password, **kwargs):
        return authenticate()
    response = {
        'token': user.generate_auth_token() + ':'
        }
    return jsonify(response)

# EOF

#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup


setup(
    name="flask-ldap-auth",
    version="0.2.4",
    py_modules=['flask_ldap_auth'],
    author="Thomas Ayih-Akakpo",
    author_email="thomas@ayih-akakpo.org",
    description=(
        "Simple Flask extension to allow "
        "authentication with a LDAP server"),
    license='MIT',
    include_package_data=True,
    install_requires=[
        'Flask',
        'python-ldap'
        ],
    url='https://github.com/drowolath/flask-ldap-auth',
    download_url='https://github.com/drowolath/flask-ldap-auth/archive/0.2.4.zip',
    keywords=['python3', 'flask', 'ldap', 'extension', 'authentication'],
    classifiers=[],
)

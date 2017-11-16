#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup


setup(
    name="flask_ldap",
    version="0.1",
    py_modules=['flask_ldap'],
    author="Thomas Ayih-Akakpo",
    author_email="thomas@ayih-akakpo.org",
    description=(
        "Simple Flask extension to allow "
        "authentication with a LDAP server"),
    license='MIT',
    include_package_data=True,
    install_requires=[
        'Flask',
        'pyldap'
        ],
    url='https://github.com/drowolath/flask-ldap',
    keywords=['python3', 'flask', 'ldap'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved ::  MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

from setuptools import  setup, find_packages
import os, sys
import codecs
#--

setup(
    name = 'demksvc',
    version = '0.6',
    keywords = ('simple', 'transform') ,
    description = 'python restful services for transforming string',
    classifiers = [
        'Programming Language :: Python :: 2.7'
    ],
    install_requires = [
        'web.py == 0.38'
    ],
    packages = find_packages(),
    platforms = 'windows',
    package_data = {
        'demksvc' : ['demk.conf', 'deMK-006', 'static/pencil.png', 'cgi-bin/deMK-ver004.exe']
    }
    
)
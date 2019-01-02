#!/usr/bin/env python
import codecs
import os.path
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


requires = ['requests>=2.20.0', "eth-keyfile==0.5.1", "secp256k1==0.13.2", "certifi==2018.4.16"]

setup_options = {
    'name': 'iconsdk', 'version': find_version("icx", "__init__.py"),
    'description': 'ICON SDK for python',
    'long_description': open('README.rst').read(),
    'author': 'ICON foundation',
    'author_email': 'foo@icon.foundation',
    'url': 'https://github.com/icon-project/icon_sdk_for_python',
    'packages': find_packages(exclude=['tests*']),
    'package_data': {'iconsdk': 'README.rst'},
    'license': "Apache License 2.0",
    'install_requires': requires,
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ]
}

setup(**setup_options)

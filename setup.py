#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import sys
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from pip.req import parse_requirements

from setuptools import find_packages
from setuptools import setup

__version__ = '0.2.10'


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

# parse_requirements() returns generator of pip.req.InstallRequirement objects
requirements = [str(ir.req) for ir in parse_requirements('./requirements.txt', session=False)]
# requirements_test = [str(ir.req) for ir in parse_requirements('./requirements-test.txt', session=False)]

setup(
    name="pyejabberd",
    version=__version__,
    license="BSD",
    description="A Python client for the Ejabberd XMLRPC API",
    long_description="%s\n%s" % (read("README.rst"), re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))),
    author="Dirk Moors",
    author_email="dirkmoors@gmail.com",
    url="https://github.com/dirkmoors/pyejabberd",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        'ejabberd', 'xmlrpc', 'api', 'client', 'xmpp', 'chat', 'muc'

    ],
    install_requires=requirements,
    extras_require={
    }
)

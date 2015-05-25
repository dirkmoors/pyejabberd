# -*- encoding: utf-8 -*-
import glob
import io
import re
import sys

import os.path
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    sys.path.append('src')
    import pyejabberd
    version = pyejabberd.__version__
except ImportError:
    version = None

if sys.argv[-1] == 'publish':
    if version is None:
        raise

    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

setup(
    name="pyejabberd",
    version=version,
    license="BSD",
    description="A Python client for the Ejabberd XMLRPC API",
    long_description="%s\n%s" % (read("README.rst"), re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))),
    author="Dirk Moors",
    author_email="dirkmoors@gmail.com",
    url="https://github.com/dirkmoors/pyejabberd",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
    ],
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
        'six>=1.9.0',
        'enum34>=1.0.4',
    ],
    extras_require={
        # eg: 'rst': ["docutils>=0.11"],
    },
    entry_points={
        "console_scripts": [
            "pyejabberd = pyejabberd.__main__:main"
        ]
    }
)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib

from six import b


def _format_digest(hexdigest):  # pragma: no cover
    parts = []
    for i in xrange(len(hexdigest) / 2):
        part = hexdigest[i * 2:(i * 2) + 2]
        if part == '00':
            part = ''
        elif part.startswith('0'):
            part = part[1:]
        parts.append(part)
    return (''.join(parts)).upper()


def _format_password_hash(password, hash_method):  # pragma: no cover
    hash_method.update(b(password))
    return _format_digest(hash_method.hexdigest())


def format_password_hash_sha(password):
    return _format_password_hash(password, hashlib.sha1())


def format_password_hash_md5(password):
    return _format_password_hash(password, hashlib.md5())

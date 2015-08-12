# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

try:
    from urllib.parse import urlparse
except ImportError:  # pragma: no cover
    from urlparse import urlparse

try:
    import xmlrpc.client as xmlrpc_client
except ImportError:  # pragma: no cover
    import xmlrpclib as xmlrpc_client

try:
    from unittest import TestCase, skipIf, main as run_unittests
except ImportError:  # pragma: no cover
    from unittest2 import TestCase, skipIf, main as run_unittests

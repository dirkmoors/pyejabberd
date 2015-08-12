# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import socket
from xmlrpc.client import ServerProxy


def ejabberd_testserver_is_up(url):
    proxy = ServerProxy(url)

    try:
        proxy._()   # Call a fictive method.
    except socket.error:
        # Not connected ; socket error mean that the service is unreachable.
        return False
    except BaseException:
        # connected to the server and the method doesn't exist which is expected.
        pass

    # Just in case the method is registered in the XmlRPC server
    return True

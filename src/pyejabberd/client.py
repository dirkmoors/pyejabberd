# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xmlrpclib
import copy

from . import contract
from .core.definitions import API, APIArgument
from .core.errors import IllegalArgumentError


# noinspection PyTypeChecker
class EjabberdAPIClient(contract.EjabberdAPIContract):
    def __init__(self, host, port, username, password, xmpp_domain, muc_service="conference", protocol='https',
                 verbose=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.xmpp_domain = xmpp_domain
        self.muc_service = muc_service
        self.protocol = protocol
        self.verbose = verbose

    @property
    def service_url(self):
        return "%s://%s:%s/" % (self.protocol, self.host, self.port)

    @property
    def proxy(self):
        return xmlrpclib.ServerProxy(self.service_url, verbose=(1 if self.verbose else 0))

    @property
    def auth(self):
        return {
            'user': self.username,
            'server': self.xmpp_domain,
            'password': self.password
        }

    def _call_api(self, api_class, **kwargs):
        assert issubclass(api_class, API)

        # Create api instance
        api = api_class()

        # Validate input
        for argument_descriptor in api.arguments:
            assert isinstance(argument_descriptor, APIArgument)

            # Validate argument presence
            if argument_descriptor.required and argument_descriptor.name not in kwargs:
                raise IllegalArgumentError('Missing required argument "%s"' % argument_descriptor.name)

        # Copy arguments
        arguments = copy.copy(kwargs)

        # Transform arguments
        arguments = api.transform_arguments(**arguments)

        # Retrieve method
        method = getattr(self.proxy, api.method)

        # Perform call
        if not api.authenticate:
            response = method(arguments)
        else:
            response = method(self.auth, arguments)

        # Validate response
        api.validate_response(response)

        # Transform response
        result = api.transform_response(response)

        return result

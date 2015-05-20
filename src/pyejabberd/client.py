# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xmlrpclib
import copy

from . import contract, definitions
from .core.definitions import API, APIArgument
from .core.errors import IllegalArgumentError


# noinspection PyTypeChecker
class EjabberdAPIClient(contract.EjabberdAPIContract):
    """
    Python Client for the Ejabberd XML-RPC API
    """
    def __init__(self, host, port, username, password, user_domain, protocol='https', verbose=False):
        """
        Constructor
        :param host:
        :type host: str
        :param port:
        :type port: int
        :param username:
        :type username: str
        :param password:
        :type password: str
        :param user_domain:
        :type user_domain: str
        :param protocol:
        :type protocol: str
        :param verbose:
        :type verbose: bool
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.user_domain = user_domain
        self.protocol = protocol
        self.verbose = verbose

    @property
    def service_url(self):
        """
        Returns the FQDN to the Ejabberd server's XML-RPC endpoint
        :return:
        """
        return "%s://%s:%s/" % (self.protocol, self.host, self.port)

    @property
    def proxy(self):
        """
        Returns the proxy object that is used to perform the calls to the XML-RPC endpoint
        :rtype: :py:class:xmlrpclib.ServerProxy
        :return the proxy object that is used to perform the calls to the XML-RPC endpoint
        """
        return xmlrpclib.ServerProxy(self.service_url, verbose=(1 if self.verbose else 0))

    @property
    def auth(self):
        """
        Returns a dictionary containing the basic authorization info
        :rtype: dict
        :return: a dictionary containing the basic authorization info
        """
        return {
            'user': self.username,
            'server': self.user_domain,
            'password': self.password
        }

    def echo(self, sentence):
        """
        Echo's the input back
        :param sentence:
        :type sentence: str
        :rtype: str
        :return: The echoed response, which should be the same as the input
        """
        return self._call_api(definitions.Echo, sentence=sentence)

    def registered_users(self, host):
        """
        List all registered users in the xmpp_host
        :param host: The XMPP_DOMAIN
        :type host: str
        :rtype: Iterable
        :return: A list of registered users in the xmpp_host
        """
        return self._call_api(definitions.RegisteredUsers, host=host)

    def register(self, user, host, password):
        """
        Registers a user to the ejabberd server
        :param user: The username for the new user
        :type user: str
        :param host: The XMPP_DOMAIN
        :type host: str
        :param password: The password for the new user
        :type password: str
        :rtype: bool
        :return: A boolean indicating if the registration has succeeded
        """
        return self._call_api(definitions.Register, user=user, host=host, password=password)

    def unregister(self, user, host):
        """
        UnRegisters a user from the ejabberd server
        :param user: The username for the new user
        :type user: str
        :param host: The XMPP_DOMAIN
        :type host: str
        :rtype: bool
        :return: A boolean indicating if the unregistration has succeeded
        """
        return self._call_api(definitions.UnRegister, user=user, host=host)

    def change_password(self, user, host, newpass):
        """
        Change the password for a given user
        :param user: The username for the user we want to change the password for
        :type user: str
        :param host: The XMPP_DOMAIN
        :type host: str
        :param newpass: The new password
        :type newpass: str
        :rtype: bool
        :return: A boolean indicating if the password change has succeeded
        """
        return self._call_api(definitions.ChangePassword, user=user, host=host, newpass=newpass)

    def check_password_hash(self, user, host, password):
        """
        Checks whether a password is correct for a given user. The used hash-method is fixed to sha1.
        :param user: The username for the user we want to check the password for
        :type user: str
        :param host: The XMPP_DOMAIN
        :type host: str
        :param password: The password we want to check for the user
        :type password: str
        :rtype: bool
        :return: A boolean indicating if the given password matches the user's password
        """
        return self._call_api(definitions.CheckPasswordHash, user=user, host=host, password=password)

    def set_nickname(self, user, host, nickname):
        """
        Set nickname in a user's vCard
        :param user: The username for the user we want to set the nickname to
        :type user: str
        :param host: The XMPP_DOMAIN
        :type host: str
        :param nickname: The nickname to assign to the user
        :type nickname: str
        :rtype: bool
        :return: A boolean indicating nickname was assigned successfully
        """
        return self._call_api(definitions.SetNickname, user=user, host=host, nickname=nickname)

    def muc_online_rooms(self, host=None):
        """
        List existing rooms ('global' to get all vhosts)
        :param host: The XMPP_DOMAIN
        :type host: str
        :rtype: Iterable
        :return: A list of online rooms in the format 'name@service'
        """
        host = host or 'global'
        return self._call_api(definitions.MucOnlineRooms, host=host)

    def create_room(self, name, service, host):
        """
        Create a MUC room name@service in host
        :param name: The name for the room
        :type name: str
        :param service: The MUC service name (e.g. "conference")
        :type service: str
        :param host: The XMPP_DOMAIN
        :type host: str
        :rtype: bool
        :return: A boolean indicating whether the room has been created successfully
        """
        return self._call_api(definitions.CreateRoom, name=name, service=service, host=host)

    def destroy_room(self, name, service, host):
        """
        Destroy a MUC room
        :param name: The name for the room
        :type name: str
        :param service: The MUC service name (e.g. "conference")
        :type service: str
        :param host: The XMPP_DOMAIN
        :type host: str
        :return:
        """
        return self._call_api(definitions.DestroyRoom, name=name, service=service, host=host)

    def _call_api(self, api_class, **kwargs):
        """
        Internal method used to perform api calls
        :param api_class:
        :type api_class: py:class:API
        :param kwargs:
        :type kwargs: dict
        :return:
        """
        # Validate api_class
        assert issubclass(api_class, API)

        # Create api instance
        api = api_class()

        # Copy arguments
        arguments = copy.copy(kwargs)

        # Transform arguments
        arguments = api.transform_arguments(**arguments)

        # Validate arguments
        for argument_descriptor in api.arguments:
            assert isinstance(argument_descriptor, APIArgument)

            # Validate argument presence
            argument_name = str(argument_descriptor.name)
            if argument_descriptor.required and argument_name not in arguments:
                raise IllegalArgumentError('Missing required argument "%s"' % argument_name)

            # Validate argument value
            argument_descriptor.validator_class().validate(arguments.get(argument_name))

        # Retrieve method
        method = getattr(self.proxy, api.method)

        # Perform call
        if not api.authenticate:
            response = method(arguments)
        else:
            response = method(self.auth, arguments)

        # Validate response
        api.validate_response(api, arguments, response)

        # Transform response
        result = api.transform_response(api, arguments, response)

        return result

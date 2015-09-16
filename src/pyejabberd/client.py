# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import copy

from builtins import range

from .compat import urlparse
from .compat import xmlrpc_client

from . import contract, definitions, defaults
from .core.definitions import API, APIArgument
from .core.errors import IllegalArgumentError


class EjabberdAPIClient(contract.EjabberdAPIContract):
    """
    Python Client for the Ejabberd XML-RPC API
    """
    def __init__(self, host, port, username, password, user_domain, protocol=None, verbose=False):
        """
        Constructor
        :param host:
        :type host: str|unicode
        :param port:
        :type port: int
        :param username:
        :type username: str|unicode
        :param password:
        :type password: str|unicode
        :param user_domain:
        :type user_domain: str|unicode
        :param protocol: http or https
        :type protocol: str|unicode
        :param verbose:
        :type verbose: bool
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.user_domain = user_domain
        self.protocol = protocol or defaults.XMLRPC_API_PROTOCOL
        self.verbose = verbose
        self._proxy = None

    @staticmethod
    def get_instance(service_url, verbose=False):
        """
        Returns a EjabberdAPIClient instance based on a '12factor app' compliant service_url

        :param service_url: A connection string in the format:
            <http|https>://<username>:<password>@<host>(:port)/user_domain
        :type service_url: str|unicode
        :param verbose:
        :type verbose: bool
        :return: EjabberdAPIClient instance
        """
        fmt_error = \
            'from_string expects service_url like https://USERNAME:PASSWORD@HOST:PORT/DOMAIN'

        o = urlparse(service_url)

        protocol = o.scheme
        assert protocol in ('http', 'https'), fmt_error

        netloc_parts = o.netloc.split('@')
        assert len(netloc_parts) == 2, fmt_error

        auth, server = netloc_parts

        auth_parts = auth.split(':')
        assert len(auth_parts) == 2, fmt_error

        username, password = auth_parts

        server_parts = server.split(':')
        assert len(server_parts) <= 2, fmt_error

        if len(server_parts) == 2:
            host, port = server_parts
            port = int(port)
        else:
            host, port = server_parts[0], defaults.XMLRPC_API_PORT

        path_parts = o.path.lstrip('/').split('/')
        assert len(path_parts) == 1, fmt_error

        user_domain = path_parts[0]

        return EjabberdAPIClient(host, port, username, password, user_domain, protocol=protocol,
                                 verbose=verbose)

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
        if self._proxy is None:
            self._proxy = xmlrpc_client.ServerProxy(self.service_url, verbose=(1 if self.verbose else 0))
        return self._proxy

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
        :type sentence: str|unicode
        :rtype: str|unicode
        :return: The echoed response, which should be the same as the input
        """
        return self._call_api(definitions.Echo, sentence=sentence)

    def registered_users(self, host):
        """
        List all registered users in the xmpp_host
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: Iterable
        :return: A list of registered users in the xmpp_host
        """
        return self._call_api(definitions.RegisteredUsers, host=host)

    def register(self, user, host, password):
        """
        Registers a user to the ejabberd server
        :param user: The username for the new user
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :param password: The password for the new user
        :type password: str|unicode
        :rtype: bool
        :return: A boolean indicating if the registration has succeeded
        """
        return self._call_api(definitions.Register, user=user, host=host, password=password)

    def unregister(self, user, host):
        """
        UnRegisters a user from the ejabberd server
        :param user: The username for the new user
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: bool
        :return: A boolean indicating if the unregistration has succeeded
        """
        return self._call_api(definitions.UnRegister, user=user, host=host)

    def change_password(self, user, host, newpass):
        """
        Change the password for a given user
        :param user: The username for the user we want to change the password for
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :param newpass: The new password
        :type newpass: str|unicode
        :rtype: bool
        :return: A boolean indicating if the password change has succeeded
        """
        return self._call_api(definitions.ChangePassword, user=user, host=host, newpass=newpass)

    def check_password_hash(self, user, host, password):
        """
        Checks whether a password is correct for a given user. The used hash-method is fixed to sha1.
        :param user: The username for the user we want to check the password for
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :param password: The password we want to check for the user
        :type password: str|unicode
        :rtype: bool
        :return: A boolean indicating if the given password matches the user's password
        """
        return self._call_api(definitions.CheckPasswordHash, user=user, host=host, password=password)

    def set_nickname(self, user, host, nickname):
        """
        Set nickname in a user's vCard
        :param user: The username for the user we want to set the nickname to
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :param nickname: The nickname to assign to the user
        :type nickname: str|unicode
        :rtype: bool
        :return: A boolean indicating nickname was assigned successfully
        """
        return self._call_api(definitions.SetNickname, user=user, host=host, nickname=nickname)

    def connected_users(self):
        """
        List all established sessions
        :rtype: list
        :return: a list of dictionaries containing user jids
        """
        return self._call_api(definitions.ConnectedUsers)

    def connected_users_info(self):
        """
        List all established sessions and their information
        :rtype: list
        :return: a list of dictionaries containing user info
        """
        return self._call_api(definitions.ConnectedUsersInfo)

    def connected_users_number(self):
        """
        Get the number of established sessions
        :rtype: int
        :return: number of established user sessions
        """
        return self._call_api(definitions.ConnectedUsersNumber)

    def user_sessions_info(self, user, host):
        """
        Get information about all sessions of a user
        :param user: The username for the user we want info for
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: list
        :return: list of information of sessions for a user
        """
        return self._call_api(definitions.UserSessionInfo, user=user, host=host)

    def muc_online_rooms(self, host=None):
        """
        List existing rooms ('global' to get all vhosts)
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: Iterable
        :return: A list of online rooms in the format 'name@service'
        """
        host = host or 'global'
        return self._call_api(definitions.MucOnlineRooms, host=host)

    def create_room(self, name, service, host):
        """
        Create a MUC room name@service in host
        :param name: The name for the room
        :type name: str|unicode
        :param service: The MUC service name (e.g. "conference")
        :type service: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: bool
        :return: A boolean indicating whether the room has been created successfully
        """
        return self._call_api(definitions.CreateRoom, name=name, service=service, host=host)

    def destroy_room(self, name, service, host):
        """
        Destroy a MUC room
        :param name: The name for the room
        :type name: str|unicode
        :param service: The MUC service name (e.g. "conference")
        :type service: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: bool
        :return: A boolean indicating whether the room has been destroyed successfully
        """
        return self._call_api(definitions.DestroyRoom, name=name, service=service, host=host)

    def get_room_options(self, name, service):
        """
        Get options from a MUC room
        :param name: The name for the room
        :type name: str|unicode
        :param service: The MUC service name (e.g. "conference")
        :type service: str|unicode
        :rtype: dict
        :return: A dict containing the room options
        """
        return self._call_api(definitions.GetRoomOptions, name=name, service=service)

    def change_room_option(self, name, service, option, value):
        """
        Change an option in a MUC room
        :param name: The name for the room
        :type name: str|unicode
        :param service: The MUC service name (e.g. "conference")
        :type service: str|unicode
        :param option: The option to change
        :type option: muc.enums.MUCRoomOption
        :param value: The new value
        :type value: str|unicode|int|bool
        :rtype: bool
        :return: A boolean indicating whether the room option has been changed successfully
        """
        return self._call_api(definitions.ChangeRoomOption, name=name, service=service, option=option, value=value)

    def set_room_affiliation(self, name, service, jid, affiliation):
        """
        Change an affiliation for a user in a MUC room
        :param name:The name for the room
        :type name: str|unicode
        :param service: The MUC service name (e.g. "conference")
        :type service: str|unicode
        :param jid: The jabber id for the user you want to change the affiliation for
        :type jid: str|unicode
        :param affiliation: The affiliation to the room
        :type affiliation: muc.enums.Affiliation
        :rtype: list
        :return: A list containing dictionaries containing affiliation info
        """
        return self._call_api(definitions.SetRoomAffiliation, name=name, service=service, jid=jid,
                              affiliation=affiliation)

    def get_room_affiliations(self, name, service):
        """
        Get the affiliations for a MUC room
        :param name:The name for the room
        :type name: str|unicode
        :param service: The MUC service name (e.g. "conference")
        :type service: str|unicode
        :return:
        """
        return self._call_api(definitions.GetRoomAffiliations, name=name, service=service)

    def add_rosteritem(self, localuser, localserver, user, server, nick, group, subs):
        """
        Add an item to a user's roster

        :param localuser: The username of user we are going to add a contact to
        :type localuser: str|unicode
        :param localserver: The XMPP_DOMAIN
        :type localserver: str|unicode
        :param user: The contact we are going to add to the user's roster
        :type user: str|unicode
        :param server: The XMPP_DOMAIN
        :type server: str|unicode
        :param nick: Nickname of the contact
        :type nick: str|unicode
        :param group: To what contact group the contact goes to
        :type group: str|unicode
        :param subs: The type of subscription
        :type subs: str|unicode
        :return:
        """
        return self._call_api(definitions.AddRosterItem,
                              localuser=localuser, localserver=localserver,
                              user=user, server=server,
                              nick=nick, group=group, subs=subs)

    def delete_rosteritem(self, localuser, localserver, user, server):
        """
        Delete an item from a user's roster

        :param localuser: The username of user we are going to delete a contact from
        :type localuser: str|unicode
        :param localserver: The XMPP_DOMAIN
        :type localserver: str|unicode
        :param user: The contact we are going to delete from the user's roster
        :type user: str|unicode
        :param server: The XMPP_DOMAIN
        :type server: str|unicode
        :return:
        """
        return self._call_api(definitions.DeleteRosterItem, localuser=localuser, localserver=localserver, user=user, server=server)

    def get_roster(self, user, host):
        """
        Get roster of a user

        :param user: The username of the user we want contact information for
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: Iterable
        :return: A list of user's contacts
        """
        return self._call_api(definitions.GetRoster, user=user, host=host)

    def _validate_and_serialize_arguments(self, api, arguments):
        """
        Internal method to validate and serialize arguments
        :param api: An instance of an API class
        :param arguments: A dictionary of arguments that will be passed to the method
        :type arguments: dict
        :rtype: dict
        :return: The serialized arguments
        """
        serialized_arguments = {}

        for i in range(len(api.arguments)):
            argument_descriptor = api.arguments[i]
            assert isinstance(argument_descriptor, APIArgument)

            # Validate argument presence
            argument_name = str(argument_descriptor.name)
            if argument_descriptor.required and argument_name not in arguments:
                raise IllegalArgumentError('Missing required argument "%s"' % argument_name)

            # Serializer argument value
            serialized_arguments[argument_descriptor.name] = \
                argument_descriptor.serializer_class().to_api(arguments.get(argument_name))

        return serialized_arguments

    def _report_method_call(self, method, arguments):
        """
        Internal method to print info about a method call
        :param method: The name oft hem ethod to call
        :type method: str|unicode
        :param arguments: A dictionary of arguments that will be passed to the method
        :type: arguments: dict
        :return:
        """
        if self.verbose:
            print('===> %s(%s)' % (method, ', '.join(['%s=%s' % (key, value) for (key, value) in arguments.items()])))

    def _call_api(self, api_class, **kwargs):
        """
        Internal method used to perform api calls
        :param api_class:
        :type api_class: py:class:API
        :param kwargs:
        :type kwargs: dict
        :rtype: object
        :return: Returns return value of the XMLRPC Method call
        """
        # Validate api_class
        assert issubclass(api_class, API)

        # Create api instance
        api = api_class()

        # Copy arguments
        arguments = copy.copy(kwargs)

        # Transform arguments
        arguments = api.transform_arguments(**arguments)

        # Validate and serialize arguments
        arguments = self._validate_and_serialize_arguments(api, arguments)

        # Retrieve method
        method = getattr(self.proxy, str(api.method))

        # Print method call with arguments
        self._report_method_call(api.method, arguments)

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

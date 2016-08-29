==============================
Python API Client for Ejabberd
==============================

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |circleci| |coveralls| |scrutinizer|
    * - package
      - |requirements| |version| |downloads| |wheel|
    * - compatibility
      - |pyversions| |implementation| |ejabberdversions|

.. |docs| image:: https://readthedocs.org/projects/pyejabberd/badge/?style=flat
    :target: https://pyejabberd.readthedocs.org/en/latest/
    :alt: Documentation Status

.. |circleci| image:: https://img.shields.io/circleci/project/dirkmoors/pyejabberd/master.svg?style=flat
    :alt: CircleCI Build Status
    :target: https://circleci.com/gh/dirkmoors/pyejabberd

.. |coveralls| image:: http://img.shields.io/coveralls/dirkmoors/pyejabberd/master.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/dirkmoors/pyejabberd

.. |version| image:: http://img.shields.io/pypi/v/pyejabberd.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pyejabberd

.. |downloads| image:: http://img.shields.io/pypi/dm/pyejabberd.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/pyejabberd

.. |wheel| image:: https://img.shields.io/pypi/wheel/pyejabberd.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pyejabberd

.. |requirements| image:: https://requires.io/github/dirkmoors/pyejabberd/requirements.svg?branch=master
     :target: https://requires.io/github/dirkmoors/pyejabberd/requirements/?branch=master
     :alt: Requirements Status

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/pyejabberd.svg?style=flat
    :alt: Supported python versions
    :target: https://pypi.python.org/pypi/pyejabberd

.. |ejabberdversions| image:: https://img.shields.io/badge/ejabberd-16.04%2C%2016.06%2C%2016.08-blue.svg
    :alt: Supported ejabberd versions
    :target: https://github.com/processone/ejabberd

.. |implementation| image:: https://img.shields.io/pypi/implementation/pyejabberd.svg?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/pyejabberd

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/dirkmoors/pyejabberd/master.png?style=flat
    :alt: Scrtinizer Status
    :target: https://scrutinizer-ci.com/g/dirkmoors/pyejabberd/

A Python client for the Ejabberd XMLRPC API

* Free software: MIT license


Installation
============

::

    pip install pyejabberd


Contributors
============

A big thanks to the contributors:

    * Jim Cortez: https://github.com/jimcortez
    * Marek Kuziel: https://github.com/encodeltd


Documentation
=============

    https://pyejabberd.readthedocs.org/


Usage
=====

.. code-block:: python

    from pyejabberd import EjabberdAPIClient

    # Create a client and authenticate with elevated user 'bob@example.com'
    client = EjabberdAPIClient(host='127.0.0.1', port=4560,
                               username='bob', password='p@$$wd',
                               user_domain='example.com',
                               protocol='https')

    # Test the connection by sending an echo request to the server
    sentence = 'some random data'
    result = client.echo(sentence)
    assert result == sentence

    # Get a list of users that are on the server
    registered_users = client.registered_users('example.com')
    # result is in the format [{'username': 'bob', ...}]

    # Register a new user
    client.register(user='alice', host='example.com', password='@l1cepwd')

    # Change a password
    client.change_password(user='alice', host='example.com', newpass='newpwd')

    # Verify password
    assert client.check_password_hash(user='bob', host='example.com', password='newpwd') is True

    # Set nickname
    client.set_nickname(user='bob', host='example.com', nickname='Bob the builder')

    # Check if Alice has an account
    client.check_account(user='alice', host='example.com')

    # Get Bob's contacts
    client.get_roster(user='bob', host='example.com')

    # Add Alice to Bob's contact group Friends
    client.add_rosteritem(localuser='bob', localserver='example.com',
                          user='alice', server='example.com', nick='Alice from Wonderland',
                          group='Friends', subs='both')

    # Delete Alice from Bob's contacts
    client.delete_rosteritem(localuser='bob', localserver='example.com',
                             user='alice', server='example.com')

    # Get list of *all* connected users
    client.connected_users()

    # Get list of *all* connected users and information about their sessions
    client.connected_users_info()

    # Get number of connected users
    client.connected_users_number()

    # Get information for all sessions for a user
    client.user_sessions_info(user="jim", host="example.com"):

    # Disconnect user's active sessions
    num_sessions = client.kick_user(user="alice", host="example.com")
    print "Number of user's sessions kicked out: {:}".format(num_sessions)

    # Disconnect user's session
    client.kick_session(user="alice", host="example.com", resource="foo", reason="bar")

    # Get muc rooms
    muc_online_rooms = client.muc_online_rooms()
    # result is in the format ['room1@conference', ...] where 'conference' is the muc service name

    # Create a muc room
    client.create_room(name='room1', service='conference', host='example.com')

    # Get room options
    room_options = client.get_room_options(name='room1', service='conference')

    # Set room option
    from pyejabberd.muc.enums import MUCRoomOption
    client.change_room_option(name='room1', service='conference', option=MUCRoomOption.public, value=False)
    client.change_room_option(name='room1', service='conference', option=MUCRoomOption.members_only, value=True)

    # Set room affiliation
    from pyejabberd.muc.enums import Affiliation
    client.set_room_affiliation(name='room1', service='conference', jid='alice@example.com', affiliation=Affiliation.member)

    # Get room affiliations
    affiliations = client.get_room_affiliations(name='room1', service='conference')

    # Destroy a muc room
    client.destroy_room(name='room1', service='conference')

    # Unregister a user
    client.unregister(user='alice', host='example.com')


Development
===========

To run the all tests run::

    tox


Ejabberd XMLRPC Setup
=====================

``Ejabberd 15.09`` introduced OAuth 2.0 implementation which also affected parts of XMLRPC implementation.

The changes mean that ``pyejabberd`` up to version ``0.2.10`` will work only with ``Ejabberd`` up to version ``15.07``.

From ``Ejabberd 15.09`` onwards:

1. Parameter ``{admin, True}`` (``'admin': True``) must be added to all admin command calls.

2. New configuration parameter ``commands_admin_access`` must specify which access group can execute admin commands.

3. Some of the commands have different arguments.

The incompatibility means that if you use ``pyejabberd 0.2.10`` and older with ``Ejabberd 15.09`` and newer
you will experience errors like::

    Error -120\nThe call provided additional unused arguments:\n[{host,<<"example.com">>}]

The previous error happens in two cases:

1. if you forget to set ``commands_admin_access`` in your ``ejabberd.yml`` with correct access group.

2. if arguments of given command changed. Eg. ``get_roster`` parameter ``host`` changed to ``server``.


Example of XMLRPC setup in ``ejabberd.yml``::

    ## enable XMLRPC module
    listen:
      ## Eg. listen for XMLRPC calls on 127.0.0.1 and
      ## allow xmlrpc_access to execute all commands
      - 
        module: ejabberd_xmlrpc
        ip: "127.0.0.1"
        port: 4560
        access_commands:
          xmlrpc_access:
            commands: all
            options: []

      ## Eg. listen for XMLRPC calls on an external IP and 
      ## allow xmlrpc_access to execute check_account command only
      - 
        module: ejabberd_xmlrpc
        ip: "192.168.1.1"
        port: 4560
        access_commands:
          xmlrpc_access:
            commands:
              - check_account
            options: []


    ## allow xmlrpc_access to execute admin commands
    commands_admin_access: xmlrpc_access


    ## set user@example.com to be part of xmlrpc_users ACL group
    acl:
      xmlrpc_users:
        user:
          - "alice": "example.com"
          - "bob": "example.com"


    ## allow users in xmlrpc_users group to commands with xmlrpc_access 
    access:
      xmlrpc_access:
        xmlrpc_users: allow


Code example illustrating the configuration and expected outcomes:

.. code-block:: python

    from pyejabberd import EjabberdAPIClient

    # API client connected to 127.0.0.1 ie. all commands allowed
    local_client = EjabberdAPIClient(host='127.0.0.1',
                                     port=4560,
                                     username='bob',
                                     password='p@$$wd',
                                     user_domain='example.com',
                                     protocol='http')

    # all commands are allowed for the client so the following will work
    print local_client.check_account('alice', 'example.com')
    # and this will work too providing the user exists of course
    print local_client.get_roster('alice', 'example.com')

    # API client connected to an external IP ie. check_account command only
    external_client = EjabberdAPIClient(host='192.168.1.1',
                                        port=4560,
                                        username='alice',
                                        password='@l1cepwd',
                                        user_domain='example.com',
                                        protocol='http')

    # only check_account command is allowed for the client so this will work
    print external_client.check_account('bob', 'example.com')
    # but this will thrown an error because of insufficient rights
    print external_client.get_roster('bob', 'example.com')


For further information about changes in ``Ejabberd 15.09`` also see:

- https://github.com/processone/ejabberd/issues/771
- https://github.com/processone/ejabberd/issues/845

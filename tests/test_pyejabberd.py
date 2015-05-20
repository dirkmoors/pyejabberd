# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest
import os
import traceback

from pyejabberd import EjabberdAPIClient, muc
from pyejabberd.errors import UserAlreadyRegisteredError

HOST = os.environ.get('PYEJABBERD_TESTS_HOST', 'localhost')
PORT = int(os.environ.get('PYEJABBERD_TESTS_PORT', 4560))
USERNAME = os.environ.get('PYEJABBERD_TESTS_USERNAME', 'admin')
PASSWORD = os.environ.get('PYEJABBERD_TESTS_PASSWORD', 'admin')
XMPP_DOMAIN = os.environ.get('PYEJABBERD_TESTS_XMPP_DOMAIN', 'example.com')
MUC_SERVICE = os.environ.get('PYEJABBERD_TESTS_MUC_SERVICE', 'conference')
PROTOCOL = os.environ.get('PYEJABBERD_TESTS_PROTOCOL', 'http')
VERBOSE = int(os.environ.get('PYEJABBERD_TESTS_VERBOSE', 0)) == 1

"""
Available commands in this ejabberd node:
   add_rosteritem localuser localserver user server nick group subs     Add an item to a user's roster (supports ODBC)
   backup file                                                          Store the database to backup file
   ban_account user host reason                                         Ban an account: kick sessions and set random password
   change_password user host newpass                                    Change the password of an account
   change_room_option name service option value                         Change an option in a MUC room
   check_account user host                                              Check if an account exists or not
   check_password user host password                                    Check if a password is correct
   check_password_hash user host passwordhash hashmethod                Check if the password hash is correct
   compile file                                                         Recompile and reload Erlang source code file
   connected_users                                                      List all established sessions
   connected_users_info                                                 List all established sessions and their information
   connected_users_number                                               Get the number of established sessions
   connected_users_vhost host                                           Get the list of established sessions in a vhost
   convert_to_yaml in out                                               Convert the input file from Erlang to YAML format
   create_room name service host                                        Create a MUC room name@service in host
   create_rooms_file file                                               Create the rooms indicated in file
   delete_expired_messages                                              Delete expired offline messages from database
   delete_old_messages days                                             Delete offline messages older than DAYS
   delete_old_users days                                                Delete users that didn't log in last days, or that never logged
   delete_old_users_vhost host days                                     Delete users that didn't log in last days in vhost, or that never logged
   delete_rosteritem localuser localserver user server                  Delete an item from a user's roster (supports ODBC)
   destroy_room name service host                                       Destroy a MUC room
   destroy_rooms_file file                                              Destroy the rooms indicated in file
   dump file                                                            Dump the database to text file
   dump_table file table                                                Dump a table to text file
   export2odbc host directory                                           Export virtual host information from Mnesia tables to SQL files
   export_odbc host file                                                Export all tables as SQL queries to a file
   export_piefxis dir                                                   Export data of all users in the server to PIEFXIS files (XEP-0227)
   export_piefxis_host dir host                                         Export data of users in a host to PIEFXIS files (XEP-0227)
   get_cookie                                                           Get the Erlang cookie of this node
   get_last user host                                                   Get last activity information (timestamp and status)
   get_loglevel                                                         Get the current loglevel
   get_room_affiliations name service                                   Get the list of affiliations of a MUC room
   get_room_occupants name service                                      Get the list of occupants of a MUC room
   get_room_occupants_number name service                               Get the number of occupants of a MUC room
   get_room_options name service                                        Get options from a MUC room
   get_roster user host                                                 Get roster of a local user
   get_user_rooms user host                                             Get the list of rooms where this user is occupant
   get_vcard user host name                                             Get content from a vCard field
   get_vcard2 user host name subname                                    Get content from a vCard field
   get_vcard2_multi user host name subname                              Get multiple contents from a vCard field
   help [--tags [tag] | com?*]                                          Show help (try: ejabberdctl help help)
   import_dir file                                                      Import users data from jabberd14 spool dir
   import_file file                                                     Import user data from jabberd14 spool file
   import_piefxis file                                                  Import users data from a PIEFXIS file (XEP-0227)
   incoming_s2s_number                                                  Number of incoming s2s connections on the node
   install_fallback file                                                Install the database from a fallback file
   kick_session user host resource reason                               Kick a user session
   kick_user user host                                                  Disconnect user's active sessions
   load file                                                            Restore the database from text file
   mnesia [info]                                                        show information of Mnesia system
   mnesia_change_nodename oldnodename newnodename oldbackup newbackup   Change the erlang node name in a backup file
   module_check module
   module_install module
   module_uninstall module
   module_upgrade module
   modules_available
   modules_installed
   modules_update_specs
   muc_online_rooms host                                                List existing rooms ('global' to get all vhosts)
   muc_unregister_nick nick                                             Unregister the nick in the MUC service
   num_active_users host days                                           Get number of users active in the last days
   num_resources user host                                              Get the number of resources of a user
   outgoing_s2s_number                                                  Number of outgoing s2s connections on the node
   privacy_set user host xmlquery                                       Send a IQ set privacy stanza for a local account
   private_get user host element ns                                     Get some information from a user private storage
   private_set user host element                                        Set to the user private storage
   process_rosteritems action subs asks users contacts                  List or delete rosteritems that match filtering options
   push_alltoall host group                                             Add all the users to all the users of Host in Group
   push_roster file user host                                           Push template roster from file to a user
   push_roster_all file                                                 Push template roster from file to all those users
   register user host password                                          Register a user
   registered_users host                                                List all registered users in HOST
   registered_vhosts                                                    List all registered vhosts in SERVER
   reload_config                                                        Reload ejabberd configuration file into memory
   remove_node node                                                     Remove an ejabberd node from Mnesia clustering config
   rename_default_nodeplugin                                            Update PubSub table from old ejabberd trunk SVN to 2.1.0
   reopen_log                                                           Reopen the log files
   resource_num user host num                                           Resource string of a session number
   restart                                                              Restart ejabberd
   restore file                                                         Restore the database from backup file
   rooms_unused_destroy host days                                       Destroy the rooms that are unused for many days in host
   rooms_unused_list host days                                          List the rooms that are unused for many days in host
   send_direct_invitation room password reason users                    Send a direct invitation to several destinations
   send_message type from to subject body                               Send a message to a local or remote bare of full JID
   send_stanza_c2s user host resource stanza                            Send a stanza as if sent from a c2s session
   set_last user host timestamp status                                  Set last activity information
   set_master nodename                                                  Set master node of the clustered Mnesia tables
   set_nickname user host nickname                                      Set nickname in a user's vCard
   set_presence user host resource type show status priority            Set presence of a session
   set_room_affiliation name service jid affiliation                    Change an affiliation in a MUC room
   set_vcard user host name content                                     Set content in a vCard field
   set_vcard2 user host name subname content                            Set content in a vCard subfield
   set_vcard2_multi user host name subname contents                     *Set multiple contents in a vCard subfield
   srg_create group host name description display                       Create a Shared Roster Group
   srg_delete group host                                                Delete a Shared Roster Group
   srg_get_info group host                                              Get info of a Shared Roster Group
   srg_get_members group host                                           Get members of a Shared Roster Group
   srg_list host                                                        List the Shared Roster Groups in Host
   srg_user_add user host group grouphost                               Add the JID user@host to the Shared Roster Group
   srg_user_del user host group grouphost                               Delete this JID user@host from the Shared Roster Group
   stats name                                                           Get statistical value: registeredusers onlineusers onlineusersnode uptimeseconds
   stats_host name host                                                 Get statistical value for this host: registeredusers onlineusers
   status                                                               Get ejabberd status
   status_list status                                                   List of logged users with this status
   status_list_host host status                                         List of users logged in host with their statuses
   status_num status                                                    Number of logged users with this status
   status_num_host host status                                          Number of logged users with this status in host
   stop                                                                 Stop ejabberd
   stop_kindly delay announcement                                       Inform users and rooms, wait, and stop the server
   unregister user host                                                 Unregister a user
   update module                                                        Update the given module, or use the keyword: all
   update_list                                                          List modified modules that can be updated
   user_resources user host                                             List user's connected resources
   user_sessions_info user host                                         Get information about all sessions of a user

"""


class EjabberdAPITests(unittest.TestCase):
    def setUp(self):
        verbose = True
        self.api = EjabberdAPIClient(
            host=HOST, port=PORT, username=USERNAME, password=PASSWORD, user_domain=XMPP_DOMAIN, protocol=PROTOCOL,
            verbose=VERBOSE)
        self.assertIsNotNone(self.api)

    def test_echo(self):
        sentence = 'TESTJE'
        result = self.api.echo(sentence)
        self.assertIsNotNone(result)
        self.assertEqual(result, sentence)

    def test_registered_users(self):
        result = self.api.registered_users(XMPP_DOMAIN)
        self.assertTrue(isinstance(result, (list, tuple)))
        self.assertTrue(self._is_registered('admin', host=XMPP_DOMAIN, registered_users=result))

    def test_register_unregister_user(self):
        username = 'test_user_123'

        result = self.api.register(username, host=XMPP_DOMAIN, password='test')
        self.assertTrue(result)
        self.assertTrue(self._is_registered(username, host=XMPP_DOMAIN))

        self._remove_user(username, host=XMPP_DOMAIN)

    def test_username_already_exists(self):
        username = 'test_user_123'

        result = self.api.register(username, host=XMPP_DOMAIN, password='test')
        self.assertTrue(result)
        self.assertTrue(self._is_registered(username, host=XMPP_DOMAIN))

        error_thrown = False
        try:
            self.api.register(username, password='test', host=XMPP_DOMAIN)
        except UserAlreadyRegisteredError:
            error_thrown = True
        self.assertTrue(error_thrown)

        self._remove_user(username, host=XMPP_DOMAIN)

    def test_change_check_password(self):
        username = 'test_user_456'

        result = self.api.register(username, host=XMPP_DOMAIN, password='test')
        self.assertTrue(result)
        self.assertTrue(self._is_registered(username, host=XMPP_DOMAIN))

        result = self.api.check_password_hash(username, host=XMPP_DOMAIN, password='test')
        self.assertTrue(result)

        result = self.api.check_password_hash(username, host=XMPP_DOMAIN, password='test2')
        self.assertFalse(result)

        result = self.api.change_password(username, host=XMPP_DOMAIN, newpass='test2')
        self.assertTrue(result)

        result = self.api.check_password_hash(username, host=XMPP_DOMAIN, password='test')
        self.assertFalse(result)

        result = self.api.check_password_hash(username, host=XMPP_DOMAIN, password='test2')
        self.assertTrue(result)

        self._remove_user(username, host=XMPP_DOMAIN)

    def test_set_nickname(self):
        username = 'test_user_789'

        result = self.api.register(username, host=XMPP_DOMAIN, password='test')
        self.assertTrue(result)
        self.assertTrue(self._is_registered(username, host=XMPP_DOMAIN))

        result = self.api.set_nickname(username, host=XMPP_DOMAIN, nickname='blabla')
        self.assertTrue(result)
        self._remove_user(username, host=XMPP_DOMAIN)

    def test_create_destroy_room(self):
        room = 'testroom_1'

        result = self.api.create_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)
        self.assertTrue(result)
        self.assertTrue(self._is_online_room(room, service=MUC_SERVICE))
        self._remove_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)

    def test_get_room_options(self):
        room = 'testroom_1'

        result = self.api.create_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)
        self.assertTrue(result)
        self.assertTrue(self._is_online_room(room, service=MUC_SERVICE))

        result = self.api.get_room_options(room, service=MUC_SERVICE)
        self.assertTrue(isinstance(result, dict))
        size = len(result)
        print(size)
        self._remove_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)


    # def test_change_room_option(self):
    #     roomjid = self._create_roomjid(roomname='testroom_3')
    #
    #     try:
    #         result = self.api.create_room(roomjid)
    #         self.assertTrue(result)
    #         self.assertTrue(self._is_online_room(roomjid))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_change_subj, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_change_subj, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_private_messages, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_private_messages, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_query_users, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_query_users, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_user_invites, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_user_invites, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.anonymous, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.anonymous, '1'))
    #
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.description, 'test description 1'))
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.description, 'test description 2: Füße'))
    #
    #         # self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.logging, '0'))
    #         # self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.logging, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.max_users, '10'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.max_users, '100'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_by_default, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_by_default, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_only, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_only, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.moderated, '1'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.moderated, '0'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password, 'abcdefg'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password, '51@#211323$%^&*()Füße'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password_protected, '1'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password_protected, '0'))
    #
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.persistent, '0'))
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.persistent, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public, '1'))
    #
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public_list, '0'))
    #         self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public_list, '1'))
    #
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject, 'test subject 1'))
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject, 'test subject 2: Füße'))
    #
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject_author, 'test author 1'))
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject_author, 'test author 2: Füße'))
    #
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.title, 'test title 1'))
    #         #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.title, 'test title 2: Füße'))
    #     except:
    #         traceback.print_exc()
    #     finally:
    #         self._remove_room(roomjid)

    def _is_registered(self, username, host, registered_users=None):
        registered_users = registered_users or self.api.registered_users(host=host)
        registered_users = [struct.get('username') for struct in registered_users]
        return username in registered_users

    def _is_online_room(self, name, service):
        online_rooms = self.api.muc_online_rooms()
        full_name = '%s@%s' % (name, service)
        return full_name in online_rooms

    def _remove_user(self, username, host):
        while True:
            result = self.api.unregister(username, host=host)
            if not result:
                continue
            if not self._is_registered(username, host=host):
                break
            print('_remove_user: retrying for username: %s' % username)

    def _remove_room(self, name, service, host):
        while True:
            result = self.api.destroy_room(name, service=service, host=host)
            if not result:
                continue
            if not self._is_online_room(name, service=service):
                break
            print('_remove_room: retrying for room: %s' % name)

if __name__ == '__main__':
    unittest.main()

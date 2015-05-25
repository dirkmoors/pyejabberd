# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest
import os
import traceback

from pyejabberd import EjabberdAPIClient
from pyejabberd.muc import MUCRoomOption
from pyejabberd.errors import UserAlreadyRegisteredError

HOST = os.environ.get('PYEJABBERD_TESTS_HOST', 'localhost')
PORT = int(os.environ.get('PYEJABBERD_TESTS_PORT', 4560))
USERNAME = os.environ.get('PYEJABBERD_TESTS_USERNAME', 'admin')
PASSWORD = os.environ.get('PYEJABBERD_TESTS_PASSWORD', 'admin')
XMPP_DOMAIN = os.environ.get('PYEJABBERD_TESTS_XMPP_DOMAIN', 'example.com')
MUC_SERVICE = os.environ.get('PYEJABBERD_TESTS_MUC_SERVICE', 'conference')
PROTOCOL = os.environ.get('PYEJABBERD_TESTS_PROTOCOL', 'http')
VERBOSE = int(os.environ.get('PYEJABBERD_TESTS_VERBOSE', 0)) == 1


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
        room = 'testroom_2'

        result = self.api.create_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)
        self.assertTrue(result)
        self.assertTrue(self._is_online_room(room, service=MUC_SERVICE))

        result = self.api.get_room_options(room, service=MUC_SERVICE)
        self.assertTrue(isinstance(result, dict))
        size = len(result)
        print(size)
        self._remove_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)


    def test_change_room_option(self):
        room = 'testroom_3'

        result = self.api.create_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)
        self.assertTrue(result)
        self.assertTrue(self._is_online_room(room, service=MUC_SERVICE))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_change_subj, value=False))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_change_subj, value=True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_private_messages, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_private_messages, value=True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_query_users, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_query_users, value=True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_user_invites, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.allow_user_invites, value=True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.anonymous, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.anonymous, value=True))

        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.description, 'test description 1'))
        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.description, 'test description 2: Füße'))

        # self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.logging, False))
        # self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.logging, True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.max_users, value=10))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.max_users, value=100))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.members_by_default, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.members_by_default, value=True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.members_only, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.members_only, value=True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.moderated, value=True))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.moderated, value=False))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.password, value='abcdefg'))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.password, value='51@#211323$%^&*()Füße'))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.password_protected, value=True))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.password_protected, value=False))

        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.persistent, False))
        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.persistent, True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.public, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.public, value=True))

        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.public_list, value=False))
        self.assertTrue(self.api.change_room_option(
            room, service=MUC_SERVICE, option=MUCRoomOption.public_list, value=True))

        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.subject, 'test subject 1'))
        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.subject, 'test subject 2: Füße'))

        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.subject_author, 'test author 1'))
        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.subject_author, 'test author 2: Füße'))

        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.title, 'test title 1'))
        #self.assertTrue(self.api.change_room_option(roomjid, MUCRoomOption.title, 'test title 2: Füße'))

        self._remove_room(room, service=MUC_SERVICE, host=XMPP_DOMAIN)

    def _is_registered(self, username, host, registered_users=None):
        registered_users = registered_users or self.api.registered_users(host=host)
        registered_users = [struct.get('username') for struct in registered_users]
        return username in registered_users

    def _is_online_room(self, name, service):
        online_rooms = self.api.muc_online_rooms()
        full_name = '%s@%s' % (name, service)
        return full_name in online_rooms

    def _remove_user(self, username, host):
        attempt = 0
        while attempt < 10:
            result = self.api.unregister(username, host=host)
            if not result:
                attempt += 1
                continue
            if not self._is_registered(username, host=host):
                break
            print('_remove_user: retrying for username: %s' % username)
            attempt += 1

    def _remove_room(self, name, service, host):
        attempt = 0
        while attempt < 10:
            result = self.api.destroy_room(name, service=service, host=host)
            if not result:
                attempt += 1
                continue
            if not self._is_online_room(name, service=service):
                break
            print('_remove_room: retrying for room: %s' % name)
            attempt += 1

if __name__ == '__main__':
    unittest.main()

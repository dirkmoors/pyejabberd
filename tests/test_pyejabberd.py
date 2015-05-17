# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest
import os

# class MainTestCase(unittest.TestCase):
#     def test_main(self):
#         self.assertEqual(main([]), 0)
from pyejabberd import EjabberdAPI, muc

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
        self.api = EjabberdAPI(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, xmpp_domain=XMPP_DOMAIN,
                               muc_service=MUC_SERVICE, protocol=PROTOCOL, verbose=VERBOSE)
        self.assertIsNotNone(self.api)

    def test_echo(self):
        sentence = 'TESTJE'
        result = self.api.echo(sentence)
        self.assertIsNotNone(result)
        self.assertEqual(result, sentence)

    def test_registered_users(self):
        result = self.api.registered_users()
        self.assertTrue(isinstance(result, (list, tuple)))
        self.assertTrue(self._is_registered('admin', registered_users=result))

    def test_register_unregister_user(self):
        username = 'test_user_123'

        try:
            result = self.api.register_user(username, password='test')
            self.assertTrue(result)
            self.assertTrue(self._is_registered(username))
        finally:
            result = self.api.unregister_user(username)
            self.assertTrue(result)
            self.assertFalse(self._is_registered(username))

    def test_change_password(self):
        username = 'test_user_456'

        try:
            result = self.api.register_user(username, password='test')
            self.assertTrue(result)
            self.assertTrue(self._is_registered(username))

            result = self.api.check_password_hash(username, password='test')
            self.assertTrue(result)
        finally:
            self._remove_user(username)

    def test_set_nickname(self):
        username = 'test_user_789'

        try:
            result = self.api.register_user(username, password='test')
            self.assertTrue(result)
            self.assertTrue(self._is_registered(username))

            result = self.api.set_nickname(username, nickname='blabla')
            self.assertTrue(result)
        finally:
            self._remove_user(username)

    def test_create_destroy_room(self):
        roomjid = self._create_roomjid(roomname='testroom_1')

        try:
            result = self.api.create_room(roomjid)
            self.assertTrue(result)
            self.assertTrue(self._is_online_room(roomjid))
        finally:
            result = self.api.destroy_room(roomjid)
            self.assertTrue(result)
            self.assertFalse(self._is_online_room(roomjid))

    def test_get_room_options(self):
        roomjid = self._create_roomjid(roomname='testroom_2')

        try:
            result = self.api.create_room(roomjid)
            self.assertTrue(result)
            self.assertTrue(self._is_online_room(roomjid))

            result = self.api.get_room_options(roomjid)
            self.assertTrue(isinstance(result, dict))
            size = len(result)
            print(size)
        finally:
            self._remove_room(roomjid)


    def test_change_room_option(self):
        roomjid = self._create_roomjid(roomname='testroom_3')

        try:
            result = self.api.create_room(roomjid)
            self.assertTrue(result)
            self.assertTrue(self._is_online_room(roomjid))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_change_subj, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_change_subj, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_private_messages, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_private_messages, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_query_users, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_query_users, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_user_invites, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.allow_user_invites, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.anonymous, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.anonymous, '1'))

            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.description, 'test description 1'))
            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.description, 'test description 2: Füße'))

            # self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.logging, '0'))
            # self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.logging, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.max_users, '10'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.max_users, '100'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_by_default, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_by_default, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_only, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.members_only, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.moderated, '1'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.moderated, '0'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password, 'abcdefg'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password, '51@#211323$%^&*()Füße'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password_protected, '1'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.password_protected, '0'))

            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.persistent, '0'))
            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.persistent, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public, '1'))

            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public_list, '0'))
            self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.public_list, '1'))

            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject, 'test subject 1'))
            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject, 'test subject 2: Füße'))

            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject_author, 'test author 1'))
            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.subject_author, 'test author 2: Füße'))

            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.title, 'test title 1'))
            #self.assertTrue(self.api.change_room_option(roomjid, muc.MUCRoomOption.title, 'test title 2: Füße'))
        finally:
            self._remove_room(roomjid)

    def _is_registered(self, username, registered_users=None):
        registered_users = registered_users or self.api.registered_users()
        registered_users = [struct.get('username') for struct in registered_users]
        return username in registered_users

    def _is_online_room(self, roomjid):
        online_rooms = self.api.list_rooms()
        return roomjid in online_rooms

    def _remove_user(self, username):
        result = self.api.unregister_user(username)
        self.assertTrue(result)
        self.assertFalse(self._is_registered(username))

    def _remove_room(self, roomjid):
        result = self.api.destroy_room(roomjid)
        self.assertTrue(result)
        self.assertFalse(self._is_online_room(roomjid))

    def _create_roomjid(self, roomname):
        return '%s@%s.%s' % (roomname, MUC_SERVICE, XMPP_DOMAIN)

if __name__ == '__main__':
    unittest.main()

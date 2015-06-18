# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import unittest
import os

from pyejabberd import EjabberdAPIClient
from pyejabberd.muc import MUCRoomOption
from pyejabberd.errors import UserAlreadyRegisteredError
from pyejabberd.core.arguments import StringArgument, BooleanArgument, IntegerArgument, PositiveIntegerArgument
from pyejabberd.muc.arguments import MUCRoomArgument
from pyejabberd.muc.enums import AllowVisitorPrivateMessage
from pyejabberd.utils import format_password_hash_md5, format_password_hash_sha

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
        sentence = '51@#211323$%^&*()üFße'
        result = self.api.echo(sentence)
        self.assertIsNotNone(result)
        self.assertEqual(result, sentence)

    def test_registered_users(self):
        result = self.api.registered_users(XMPP_DOMAIN)
        self.assertTrue(isinstance(result, (list, tuple)))

        registered_users = self.api.registered_users(host=XMPP_DOMAIN)
        registered_users = [struct.get('username') for struct in registered_users]
        self.assertTrue('admin' in registered_users)

    def test_register_unregister_user(self):
        with create_test_user(self.api, 'testuser_1', host=XMPP_DOMAIN) as username:
            registered_users = self.api.registered_users(host=XMPP_DOMAIN)
            registered_users = [struct.get('username') for struct in registered_users]
            self.assertTrue(username in registered_users)

    def test_username_already_exists(self):
        with create_test_user(self.api, 'testuser_2', host=XMPP_DOMAIN) as username:
            error_thrown = False
            try:
                with create_test_user(self.api, 'testuser_2', host=XMPP_DOMAIN) as username2:
                    self.assertEqual(username2, username)
            except UserAlreadyRegisteredError:
                error_thrown = True
            self.assertTrue(error_thrown)

    def test_change_check_password(self):
        with create_test_user(self.api, 'testuser_3', host=XMPP_DOMAIN, password='test') as username:
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

    def test_set_nickname(self):
        with create_test_user(self.api, 'testuser_4', host=XMPP_DOMAIN) as username:
            result = self.api.set_nickname(username, host=XMPP_DOMAIN, nickname='blabla')
            self.assertTrue(result)

    def test_create_destroy_room(self):
        with create_test_room(self.api, 'testroom_1', service=MUC_SERVICE, host=XMPP_DOMAIN,
                              test_existence=False) as room:
            online_rooms = self.api.muc_online_rooms()
            full_name = '%s@%s' % (room, MUC_SERVICE)
            self.assertTrue(full_name in online_rooms)

    def test_get_room_options(self):
        with create_test_room(self.api, 'testroom_2', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            result = self.api.get_room_options(room, service=MUC_SERVICE)
            self.assertTrue(isinstance(result, dict))

    def test_room_option_allow_change_subj(self):
        with create_test_room(self.api, 'testroom_3', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_change_subj, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_change_subj, value=True))

    def test_room_option_allow_private_messages(self):
        with create_test_room(self.api, 'testroom_4', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_private_messages, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_private_messages, value=True))

    def test_room_option_allow_query_users(self):
        with create_test_room(self.api, 'testroom_5', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_query_users, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_query_users, value=True))

    def test_room_option_allow_user_invites(self):
        with create_test_room(self.api, 'testroom_6', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_user_invites, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_user_invites, value=True))

    def test_room_option_allow_visitor_nickchange(self):
        with create_test_room(self.api, 'testroom_7', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_visitor_nickchange, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_visitor_nickchange, value=True))

    def test_room_option_allow_visitor_status(self):
        with create_test_room(self.api, 'testroom_8', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_visitor_status, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_visitor_status, value=True))

    def test_room_option_anonymous(self):
        with create_test_room(self.api, 'testroom_9', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.anonymous, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.anonymous, value=True))

    def test_room_option_captcha_protected(self):
        with create_test_room(self.api, 'testroom_10', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.captcha_protected, value=True))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.captcha_protected, value=False))

    def test_room_option_logging(self):
        with create_test_room(self.api, 'testroom_11', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.logging, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.logging, value=True))

    def test_room_option_max_users(self):
        with create_test_room(self.api, 'testroom_12', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.max_users, value=10))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.max_users, value=100))

    def test_room_option_members_by_default(self):
        with create_test_room(self.api, 'testroom_13', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.members_by_default, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.members_by_default, value=True))

    def test_room_option_members_only(self):
        with create_test_room(self.api, 'testroom_14', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.members_only, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.members_only, value=True))

    def test_room_option_moderated(self):
        with create_test_room(self.api, 'testroom_15', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.moderated, value=True))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.moderated, value=False))

    def test_room_option_password(self):
        with create_test_room(self.api, 'testroom_16', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.password, value='abcdefg'))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.password, value='51@#211323$%^&*()üFße'))

    def test_room_option_password_protected(self):
        with create_test_room(self.api, 'testroom_17', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.password_protected, value=True))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.password_protected, value=False))

    def test_room_option_persistent(self):
        with create_test_room(self.api, 'testroom_18', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.persistent, value=True))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.persistent, value=False))

    def test_room_option_public(self):
        with create_test_room(self.api, 'testroom_19', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.public, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.public, value=True))

    def test_room_option_public_list(self):
        with create_test_room(self.api, 'testroom_20', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.public_list, value=False))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.public_list, value=True))

    def test_room_option_title(self):
        with create_test_room(self.api, 'testroom_21', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.title, value='51@#211323$%^&*()üFße'))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.title, value='abcdefg'))

    def test_room_option_allow_private_messages_from_visitors(self):
        with create_test_room(self.api, 'testroom_22', service=MUC_SERVICE, host=XMPP_DOMAIN) as room:
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_private_messages_from_visitors,
                value=AllowVisitorPrivateMessage.nobody))
            self.assertTrue(self.api.change_room_option(
                room, service=MUC_SERVICE, option=MUCRoomOption.allow_private_messages_from_visitors,
                value=AllowVisitorPrivateMessage.moderators))


class LibraryTests(unittest.TestCase):
    def test_string_argument(self):
        serializer = self._test_argument_and_get_serializer(StringArgument)

        result = serializer.to_api('abc')
        self.assertEqual(result, 'abc')

        result = serializer.to_python('abc')
        self.assertEqual(result, 'abc')

        error_thrown = False
        try:
            serializer.to_api(123)
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

        error_thrown = False
        try:
            serializer.to_python(False)
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

    def test_integer_argument(self):
        serializer = self._test_argument_and_get_serializer(IntegerArgument)

        result = serializer.to_api(123)
        self.assertEqual(result, '123')

        result = serializer.to_python('-123')
        self.assertEqual(result, -123)

        error_thrown = False
        try:
            serializer.to_api('123')
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

        error_thrown = False
        try:
            serializer.to_python('bla')
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

    def test_positive_integer_argument(self):
        serializer = self._test_argument_and_get_serializer(PositiveIntegerArgument)

        result = serializer.to_api(123)
        self.assertEqual(result, '123')

        result = serializer.to_python('123')
        self.assertEqual(result, 123)

        error_thrown = False
        try:
            serializer.to_api(-15)
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

        error_thrown = False
        try:
            serializer.to_python('-123')
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

    def test_boolean_argument(self):
        serializer = self._test_argument_and_get_serializer(BooleanArgument)

        result = serializer.to_api(True)
        self.assertEqual(result, 'true')

        result = serializer.to_api(False)
        self.assertEqual(result, 'false')

        result = serializer.to_python('true')
        self.assertEqual(result, True)

        result = serializer.to_python('false')
        self.assertEqual(result, False)

        error_thrown = False
        try:
            serializer.to_api(-15)
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

        error_thrown = False
        try:
            serializer.to_python('123')
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

    def test_mucroom_argument(self):
        serializer = self._test_argument_and_get_serializer(MUCRoomArgument)

        result = serializer.to_api(MUCRoomOption.allow_change_subj)
        self.assertEqual(result, 'allow_change_subj')

        result = serializer.to_api(MUCRoomOption.allow_change_subj.name)
        self.assertEqual(result, 'allow_change_subj')

        result = serializer.to_python('allow_change_subj')
        self.assertEqual(result, MUCRoomOption.allow_change_subj)

        error_thrown = False
        try:
            serializer.to_api(-15)
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

        error_thrown = False
        try:
            serializer.to_python('123')
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

        error_thrown = False
        try:
            serializer.to_python({})
        except ValueError:
            error_thrown = True
        self.assertTrue(error_thrown)

    def test_sha_hash(self):
        result = format_password_hash_sha('test')
        self.assertEqual(str(result), 'A94A8FE5CCB19BA61C4C873D391E987982FBBD3')

    def test_md5_hash(self):
        result = format_password_hash_md5('test')
        self.assertEqual(str(result), '98F6BCD4621D373CADE4E832627B4F6')

    def _test_argument_and_get_serializer(self, argument_class):
        arg_name = 'arg_name'
        arg_description = 'arg_description'
        arg_required = True

        # Test constructor
        arg = argument_class(arg_name, arg_description, arg_required)
        self.assertEqual(arg.name, arg_name)
        self.assertEqual(arg.description, arg_description)
        self.assertEqual(arg.required, arg_required)

        # Test Serializer class presence
        serializer_class = arg.serializer_class
        self.assertIsNotNone(serializer_class)

        # Test Serializer
        serializer = serializer_class()

        return serializer


class create_test_user(object):
    def __init__(self, api, username, host, password='test', test_existence=True):
        self.api = api
        self.username = username
        self.host = host
        self.password = password
        self.test_existence = test_existence

    def _is_registered(self, username, host, registered_users=None):
        registered_users = registered_users or self.api.registered_users(host=host)
        registered_users = [struct.get('username') for struct in registered_users]
        return username in registered_users

    def _remove_user(self, username, host):  # pragma: no cover
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

    def __enter__(self):
        self.api.register(self.username, host=self.host, password=self.password)

        if self.test_existence:
            if not self._is_registered(self.username, host=self.host):
                raise AssertionError('newly created user is not found in registered users')

        return self.username

    def __exit__(self, type, value, traceback):
        self._remove_user(self.username, host=self.host)


class create_test_room(object):
    def __init__(self, api, room, service, host, test_existence=True):
        self.api = api
        self.room = room
        self.service = service
        self.host = host
        self.test_existence = test_existence

    def _is_online_room(self, name, service):
        online_rooms = self.api.muc_online_rooms()
        full_name = '%s@%s' % (name, service)
        return full_name in online_rooms

    def _remove_room(self, name, service, host):  # pragma: no cover
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

    def __enter__(self):
        self.api.create_room(self.room, service=self.service, host=self.host)

        if self.test_existence:
            if not self._is_online_room(self.room, service=self.service):
                raise AssertionError('newly created room is not online')

        return self.room

    def __exit__(self, type, value, traceback):
        self._remove_room(self.room, service=self.service, host=self.host)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import six
import logging
import xmlrpclib

from .core import XMPPServerAPI, muc
from .utils import format_password_hash_sha
from .errors import UnexpectedStatusError

logger = logging.getLogger(__name__)


class EjabberdAPI(XMPPServerAPI):
    def __init__(self, host, port, username, password, xmpp_domain, muc_service="conference", protocol='https',
                 verbose=False):

        logger.info('EjabberdAPI(host: %s, port: %s, username: %s, password: *******, xmpp_domain: %s, '
                    'muc_service=%s, protocol=%s, verbose: %s)' % (host, port, username, xmpp_domain, muc_service,
                                                                   protocol, verbose))

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

    def echo(self, sentence):
        response = self.proxy.echothisnew({
            'sentence': sentence
        })
        return response.get('repeated')

    def registered_users(self):
        response = self.proxy.registered_users(self.auth, {
            'host': self.xmpp_domain
        })
        return response.get('users', [])

    def register_user(self, username, password):
        response = self.proxy.register(self.auth, {
            'user': username,
            'host': self.xmpp_domain,
            'password': password
        })
        result = response.get("res", -1)
        if result == 1:
            # User already exists, so update his password
            return self.change_password(username, password)
        return result == 0

    def change_password(self, username, password):
        response = self.proxy.change_password(self.auth, {
            'user': username,
            'host': self.xmpp_domain,
            'newpass': password
        })
        return response.get('res', -1) == 0

    def unregister_user(self, username):
        response = self.proxy.unregister(self.auth, {
            'user': username,
            'host': self.xmpp_domain
        })
        return response.get("res", -1) == 0

    def check_password_hash(self, username, password):
        passwordhash = format_password_hash_sha(password=password)
        response = self.proxy.check_password_hash(self.auth, {
            'user': username,
            'host': self.xmpp_domain,
            'passwordhash': passwordhash,
            'hashmethod': 'sha'
        })
        return response.get("res", -1) == 0

    def set_nickname(self, username, nickname):
        response = self.proxy.set_nickname(self.auth, {
            'user': username,
            'host': self.xmpp_domain,
            'nickname': nickname
        })
        return response.get("res", -1) == 0

    def create_room(self, roomjid):
        name = self._jid_to_name(roomjid)
        service = self.muc_service
        host = self.xmpp_domain
        assert roomjid == '%s@%s.%s' % (name, service, host)

        data = {
            'name': name,
            'service': service,
            'host': host
        }
        response = self.proxy.create_room(self.auth, data)
        return response.get("res", -1) == 0

    def destroy_room(self, roomjid):
        name = self._jid_to_name(roomjid)
        service = self.muc_service
        host = self.xmpp_domain
        assert roomjid == '%s@%s.%s' % (name, service, host)

        data = {
            'name': name,
            'service': service,
            'host': host
        }
        response = self.proxy.destroy_room(self.auth, data)
        return response.get("res", -1) == 0

    def list_rooms(self):
        data = {
            'host': 'global',
        }
        response = self.proxy.muc_online_rooms(self.auth, data)
        return ["%s@%s.%s" % (
            self._jid_to_name(result_dict.get('room')), self.muc_service, self.xmpp_domain,
        ) for result_dict in response.get('rooms', {})]

    def get_room_options(self, roomjid):
        name = self._jid_to_name(roomjid)
        service = self.muc_service
        host = self.xmpp_domain
        assert roomjid == '%s@%s.%s' % (name, service, host)

        data = {
            'name': name,
            'service': service
        }
        response = self.proxy.get_room_options(self.auth, data)

        result = {}
        for option_dict in response.get('options', []):
            option = option_dict.get('option', None)
            if option is None:
                continue
            name_dict, value_dict = option
            result[name_dict['name']] = value_dict['value']
        return result

    def change_room_option(self, roomjid, option, value):
        name = self._jid_to_name(roomjid)
        service = self.muc_service
        host = self.xmpp_domain
        assert roomjid == '%s@%s.%s' % (name, service, host)
        assert isinstance(option, muc.MUCRoomOption)
        assert isinstance(value, six.string_types)

        data = {
            'name': name,
            'service': service,
            'option': option.name,
            'value': value
        }
        response = self.proxy.change_room_option(self.auth, data)
        return response.get("res", -1) == 0

    def _expect_result_code(self, func_name, response, expected_result_code=0):
        if response.get("res") != expected_result_code:
            logger.error("Unexpected status: %s: %s" % (response.get("res"), response.get("text")))
            raise UnexpectedStatusError("%s: result_code: %s" % (func_name, response.response.get("res")))

    def _jid_to_name(self, jid):
        assert '@' in jid
        return jid.split('@')[0]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass


class EjabberdAPIContract(with_metaclass(ABCMeta, object)):  # pragma: no cover
    @abstractmethod
    def echo(self, sentence):
        pass

    @abstractmethod
    def registered_users(self, host):
        pass

    @abstractmethod
    def register(self, user, host, password):
        pass

    @abstractmethod
    def unregister(self, user, host):
        pass

    @abstractmethod
    def change_password(self, user, host, newpass):
        pass

    @abstractmethod
    def check_password_hash(self, user, host, password):
        pass

    @abstractmethod
    def set_nickname(self, user, host, nickname):
        pass

    @abstractmethod
    def muc_online_rooms(self, host=None):
        pass

    @abstractmethod
    def create_room(self, name, service, host):
        pass

    @abstractmethod
    def destroy_room(self, name, service, host):
        pass

    @abstractmethod
    def get_room_options(self, name, service):
        pass

    @abstractmethod
    def change_room_option(self, name, service, option, value):
        pass

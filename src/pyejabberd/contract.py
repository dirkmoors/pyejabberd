# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass


class EjabberdAPIContract(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def echo(self, sentence):
        pass

    @abstractmethod
    def registered_users(self):
        pass

    @abstractmethod
    def register(self, user, password):
        pass

    @abstractmethod
    def unregister(self, user):
        pass

    @abstractmethod
    def change_password(self, user, newpass):
        pass

    @abstractmethod
    def check_password_hash(self, user, password):
        pass

    @abstractmethod
    def set_nickname(self, user, nickname):
        pass

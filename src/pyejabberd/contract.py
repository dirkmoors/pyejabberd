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

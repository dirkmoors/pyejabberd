# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from six import with_metaclass
from abc import ABCMeta, abstractmethod

from .enums import AllowVisitorPrivateMessage


class MUCRoomOptionSerializer(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def to_api(self, python_value):
        pass

    @abstractmethod
    def to_python(self, api_value):
        pass


class StringSerializer(MUCRoomOptionSerializer):
    def to_api(self, python_value):
        return python_value

    def to_python(self, api_value):
        return api_value


class IntegerSerializer(MUCRoomOptionSerializer):
    def to_api(self, python_value):
        assert isinstance(python_value, (int, long))
        return str(python_value)

    def to_python(self, api_value):
        return int(api_value)


class PositiveIntegerSerializer(IntegerSerializer):
    def to_api(self, python_value):
        assert isinstance(python_value, (int, long))
        assert python_value >= 0
        return super(PositiveIntegerSerializer, self).to_api(python_value)


class BooleanSerializer(MUCRoomOptionSerializer):
    def to_api(self, python_value):
        assert isinstance(python_value, bool)
        return 'true' if python_value else 'false'

    def to_python(self, api_value):
        return api_value == 'true'


class AllowVisitorPrivateMessageSerializer(StringSerializer):
    def to_api(self, python_value):
        assert isinstance(python_value, AllowVisitorPrivateMessage)
        return python_value

    def to_python(self, api_value):
        return getattr(AllowVisitorPrivateMessage, api_value)

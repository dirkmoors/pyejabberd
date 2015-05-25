# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from abc import ABCMeta, abstractproperty
from six import with_metaclass, string_types

from .definitions import Enum, APIArgumentSerializer


class StringSerializer(APIArgumentSerializer):
    def to_api(self, python_value):
        return python_value

    def to_python(self, api_value):
        return api_value


class IntegerSerializer(APIArgumentSerializer):
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


class BooleanSerializer(APIArgumentSerializer):
    def to_api(self, python_value):
        assert isinstance(python_value, bool)
        return 'true' if python_value else 'false'

    def to_python(self, api_value):
        return api_value == 'true'


class EnumSerializer(with_metaclass(ABCMeta, StringSerializer)):
    @abstractproperty
    def enum_class(self):
        pass

    def to_api(self, python_value):
        assert issubclass(self.enum_class, Enum)
        if isinstance(python_value, self.enum_class):
            return python_value.name
        elif isinstance(python_value, string_types):
            return python_value
        elif isinstance(python_value, int):
            return self.enum_class.get_by_value(python_value).name
        raise ValueError('Invalid value for MUCRoomOptionSerializer: %s' % python_value)

    def to_python(self, api_value):
        assert issubclass(self.enum_class, Enum)
        return self.enum_class.get_by_name(api_value)

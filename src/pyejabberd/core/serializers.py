# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from abc import ABCMeta, abstractproperty
from six import with_metaclass, string_types

from .definitions import Enum, APIArgumentSerializer


class StringSerializer(APIArgumentSerializer):
    def to_api(self, python_value):
        if not isinstance(python_value, string_types):
            raise ValueError('Invalid value. Expects str or unicode.')
        return python_value

    def to_python(self, api_value):
        if not isinstance(api_value, string_types):
            raise ValueError('Invalid value. Expects str or unicode.')
        return api_value


class IntegerSerializer(APIArgumentSerializer):
    def to_api(self, python_value):
        if not isinstance(python_value, (int, long)):
            raise ValueError('Invalid value. Expects int or long.')
        return str(python_value)

    def to_python(self, api_value):
        return int(api_value)


class PositiveIntegerSerializer(IntegerSerializer):
    def to_api(self, python_value):
        if not isinstance(python_value, (int, long)) or python_value < 0:
            raise ValueError('Invalid value. Expects positive int or long.')
        return super(PositiveIntegerSerializer, self).to_api(python_value)

    def to_python(self, api_value):
        result = super(PositiveIntegerSerializer, self).to_python(api_value)
        if result < 0:
            raise ValueError('Invalid value. Expects positive int or long.')
        return result


class BooleanSerializer(APIArgumentSerializer):
    def to_api(self, python_value):
        if not isinstance(python_value, bool):
            raise ValueError('Invalid value. Expects bool.')
        return 'true' if python_value else 'false'

    def to_python(self, api_value):
        if api_value not in ('true', 'false'):
            raise ValueError('Invalid value. Expects true|false.')
        return api_value == 'true'


class EnumSerializer(with_metaclass(ABCMeta, StringSerializer)):
    @abstractproperty
    def enum_class(self):  # pragma: no cover
        pass

    def to_api(self, python_value):
        assert issubclass(self.enum_class, Enum)
        if isinstance(python_value, self.enum_class):
            return python_value.name
        elif isinstance(python_value, string_types):
            return python_value
        elif isinstance(python_value, int):
            return self.enum_class.get_by_value(python_value).name
        raise ValueError('Invalid value for enum %s: %s' % (self.enum_class, python_value))

    def to_python(self, api_value):
        assert issubclass(self.enum_class, Enum)
        if not isinstance(api_value, string_types):
            raise ValueError('Invalid value. Expects str or unicode')
        result = self.enum_class.get_by_name(api_value)
        if result is None:
            raise ValueError('Invalid value. Expects enum value for %s.' % self.enum_class)
        return result

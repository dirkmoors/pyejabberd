# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .definitions import APIArgumentValidator


class StringValidator(APIArgumentValidator):
    def validate(self, python_value):
        return python_value


class IntegerValidator(APIArgumentValidator):
    def validate(self, python_value):
        assert isinstance(python_value, (int, long))


class PositiveIntegerValidator(IntegerValidator):
    def validate(self, python_value):
        assert isinstance(python_value, (int, long))
        assert python_value >= 0
        return super(PositiveIntegerValidator, self).validate(python_value)


class BooleanValidator(APIArgumentValidator):
    def validate(self, python_value):
        assert isinstance(python_value, bool)

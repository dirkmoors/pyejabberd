# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .definitions import APIArgument
from .validators import StringValidator, IntegerValidator, PositiveIntegerValidator, BooleanValidator


class StringArgument(APIArgument):
    validator_class = StringValidator


class IntegerArgument(APIArgument):
    validator_class = IntegerValidator


class PositiveIntegerArgument(APIArgument):
    validator_class = PositiveIntegerValidator


class BooleanArgument(APIArgument):
    validator_class = BooleanValidator

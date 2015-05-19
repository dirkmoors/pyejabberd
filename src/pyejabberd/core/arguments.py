# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .definitions import APIArgument
from .serializers import StringSerializer, IntegerSerializer, PositiveIntegerSerializer, BooleanSerializer


class StringArgument(APIArgument):
    serializer_class = StringSerializer


class IntegerArgument(APIArgument):
    serializer_class = IntegerSerializer


class PositiveIntegerArgument(APIArgument):
    serializer_class = PositiveIntegerSerializer


class BooleanArgument(APIArgument):
    serializer_class = BooleanSerializer

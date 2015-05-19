# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .core.arguments import StringArgument, IntegerArgument, PositiveIntegerArgument, BooleanArgument
from .core.definitions import API


class Echo(API):
    method = 'echothisnew'
    arguments = [StringArgument('sentence')]

    def transform_response(self, response):
        return response.get('repeated')



API = [
    Echo,
]

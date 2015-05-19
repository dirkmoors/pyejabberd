# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .core.arguments import StringArgument, IntegerArgument, PositiveIntegerArgument, BooleanArgument
from .core.definitions import API


class Echo(API):
    method = 'echothisnew'
    arguments = [StringArgument('sentence')]

    def transform_response(self, context, response):
        return response.get('repeated')


class RegisteredUsers(API):
    method = 'registered_users'
    arguments = []

    def transform_arguments(self, context, **kwargs):
        kwargs.update({
            'host': context.get('host')
        })
        return kwargs

    def transform_response(self, context, response):
        return response.get('users', [])

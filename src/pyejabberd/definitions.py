# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .core.arguments import StringArgument, IntegerArgument, PositiveIntegerArgument, BooleanArgument
from .core.definitions import API

from .errors import UserAlreadyRegisteredError


class Echo(API):
    method = 'echothisnew'
    arguments = [StringArgument('sentence')]

    def transform_response(self, context, api, arguments, response):
        return response.get('repeated')


class RegisteredUsers(API):
    method = 'registered_users'
    arguments = []

    def transform_arguments(self, context, **kwargs):
        kwargs.update({
            'host': context.get('host')
        })
        return kwargs

    def transform_response(self, context, api, arguments, response):
        return response.get('users', [])


class Register(API):
    method = 'register'
    arguments = [StringArgument('user'), StringArgument('password')]

    def transform_arguments(self, context, **kwargs):
        kwargs.update({
            'host': context.get('host')
        })
        return kwargs

    def validate_response(self, context, api, arguments, response):
        if response.get('res') == 1:
            username = arguments.get('user')
            raise UserAlreadyRegisteredError('User with username %s already exists' % username)

    def transform_response(self, context, api, arguments, response):
        return response.get('res') == 0


class UnRegister(API):
    method = 'unregister'
    arguments = [StringArgument('user')]

    def transform_arguments(self, context, **kwargs):
        kwargs.update({
            'host': context.get('host')
        })
        return kwargs

    def transform_response(self, context, api, arguments, response):
        return response.get('res') == 0

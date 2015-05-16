# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six

from .enums import MUCRoomOption
from .serializers import BooleanSerializer, StringSerializer, PositiveIntegerSerializer, \
    AllowVisitorPrivateMessageSerializer


MUCRoomOptions = {
    MUCRoomOption.allow_change_subj.name:                    BooleanSerializer,
    MUCRoomOption.allow_private_messages.name:               BooleanSerializer,
    MUCRoomOption.allow_private_messages_from_visitors.name: AllowVisitorPrivateMessageSerializer,
    MUCRoomOption.allow_query_users.name:                    BooleanSerializer,
    MUCRoomOption.allow_user_invites.name:                   BooleanSerializer,
    MUCRoomOption.allow_visitor_nickchange.name:             BooleanSerializer,
    MUCRoomOption.allow_visitor_status.name:                 BooleanSerializer,
    MUCRoomOption.allow_voice_requests.name:                 BooleanSerializer,
    MUCRoomOption.anonymous.name:                            BooleanSerializer,
    MUCRoomOption.captcha_protected.name:                    BooleanSerializer,
    MUCRoomOption.captcha_whitelist.name:                    StringSerializer,
    MUCRoomOption.description.name:                          StringSerializer,
    MUCRoomOption.logging.name:                              BooleanSerializer,
    MUCRoomOption.max_users.name:                            PositiveIntegerSerializer,
    MUCRoomOption.members_by_default.name:                   BooleanSerializer,
    MUCRoomOption.members_only.name:                         BooleanSerializer,
    MUCRoomOption.moderated.name:                            BooleanSerializer,
    MUCRoomOption.password.name:                             StringSerializer,
    MUCRoomOption.password_protected.name:                   BooleanSerializer,
    MUCRoomOption.persistent.name:                           BooleanSerializer,
    MUCRoomOption.public.name:                               BooleanSerializer,
    MUCRoomOption.public_list.name:                          BooleanSerializer,
    MUCRoomOption.title.name:                                StringSerializer,
    MUCRoomOption.vcard.name:                                StringSerializer,
    MUCRoomOption.voice_request_min_interval.name:           PositiveIntegerSerializer
}


def get_serializer(option):
    serializer_class = None
    if isinstance(option, six.string_types):
        serializer_class = MUCRoomOptions.get(option)
    elif isinstance(option, MUCRoomOption):
        serializer_class = MUCRoomOptions.get(option.name)

    if serializer_class is None:
        raise ValueError('Unknown option')

    return serializer_class()


def to_python(option, value):
    serializer = get_serializer(option)
    return serializer.to_python(value)


def to_api(option, value):
    serializer = get_serializer(option)
    return serializer.to_api(value)

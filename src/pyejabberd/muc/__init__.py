# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..core.serializers import BooleanSerializer, StringSerializer, PositiveIntegerSerializer
from .serializers import AllowVisitorPrivateMessageSerializer
from .enums import MUCRoomOption


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

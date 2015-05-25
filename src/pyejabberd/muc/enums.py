# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..core.definitions import Enum


MUCRoomOption = Enum(
    'MUCRoomOption',
    ' '.join([
        'allow_change_subj',
        'allow_private_messages',
        'allow_private_messages_from_visitors',
        'allow_query_users',
        'allow_user_invites',
        'allow_visitor_nickchange',
        'allow_visitor_status',
        'allow_voice_requests',
        'anonymous',
        'captcha_protected',
        'captcha_whitelist',
        'description',
        'logging',
        'max_users',
        'members_by_default',
        'members_only',
        'moderated',
        'password',
        'password_protected',
        'persistent',
        'public',
        'public_list',
        'title',
        'vcard',
        'voice_request_min_interval',
    ]),
    module=__name__)


AllowVisitorPrivateMessage = Enum(
    'AllowVisitorPrivateMessage',
    'anyone moderators nobody',
    module=__name__)

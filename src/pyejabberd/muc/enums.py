# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..core.definitions import Enum


class MUCRoomOption(Enum):
    allow_change_subj = 1
    allow_private_messages = 2
    allow_private_messages_from_visitors = 3
    allow_query_users = 4
    allow_user_invites = 5
    allow_visitor_nickchange = 6
    allow_visitor_status = 7
    anonymous = 8
    captcha_protected = 9
    logging = 10
    max_users = 11
    members_by_default = 12
    members_only = 13
    moderated = 14
    password = 15
    password_protected = 16
    persistent = 17
    public = 18
    public_list = 19
    title = 20


class AllowVisitorPrivateMessage(Enum):
    anyone = 1
    moderators = 2
    nobody = 3

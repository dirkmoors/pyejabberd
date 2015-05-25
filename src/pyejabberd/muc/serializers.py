# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..core.serializers import EnumSerializer
from .enums import MUCRoomOption, AllowVisitorPrivateMessage


class MUCRoomOptionSerializer(EnumSerializer):
    enum_class = MUCRoomOption


class AllowVisitorPrivateMessageSerializer(EnumSerializer):
    enum_class = AllowVisitorPrivateMessage

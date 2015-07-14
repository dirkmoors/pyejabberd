# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..core.definitions import APIArgument
from .serializers import MUCRoomOptionSerializer, AffiliationSerializer


class MUCRoomArgument(APIArgument):
    serializer_class = MUCRoomOptionSerializer


class AffiliationArgument(APIArgument):
    serializer_class = AffiliationSerializer

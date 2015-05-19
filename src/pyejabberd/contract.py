# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from abc import ABCMeta
from six import with_metaclass


class EjabberdAPIContract(with_metaclass(ABCMeta, object)):
    def echo(self, sentence):
        pass

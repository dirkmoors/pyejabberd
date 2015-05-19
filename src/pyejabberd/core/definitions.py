# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from abc import ABCMeta, abstractproperty, abstractmethod
from six import with_metaclass


class APIArgumentSerializer(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def to_api(self, python_value):
        """
        """
        pass

    @abstractmethod
    def to_python(self, api_value):
        pass


class APIArgument(with_metaclass(ABCMeta, object)):
    def __init__(self, name, description=None, required=True):
        self.name = name
        self.description = description
        self.required = required

    @abstractproperty
    def serializer_class(self):
        pass


class API(with_metaclass(ABCMeta, object)):
    @abstractproperty
    def method(self):
        """
        Returns the exact name of the XMLRPC API method to call
        :rtype: str
        :return: Name of the XMLRPC API method to call
        """

    @abstractproperty
    def arguments(self):
        """
        Returns an (ordered) list of APIArgument objects.
        :rtype: Iterable
        :return: An iterable containing the arguments
        """

    @property
    def authenticate(self):
        """
        Defines whether or not we should authenticate when calling this API
        :return:
        """
        return True

    def transform_arguments(self, **kwargs):
        """
        Handler method to transform an argument before processing
        :param kwargs: Named argument dictionary
        :return:
        """
        return kwargs

    def validate_response(self, response):
        """
        Handler to validate the API response. Can be used to raise an exception to indicate failure. If it does not
          raise an exception, the pipeline will continue with the 'transform_response' method.
        :param response:
        :return:
        """

    def transform_response(self, response):
        """
        Handler method to process the response. The output of this method will be returned as the output of the API
          call.
        :param response:
        :return:
        """
        return response

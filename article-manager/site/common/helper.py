# coding: utf-8
# helper functions
from rest_framework import serializers

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user or request.user,
    }

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class RestfulJsonField(serializers.Field):
    """
    load and dump json object to overcome the encoding problem for python2
    """
    def to_representation(self, obj):
        # 'obj' should be a unicode string
        # print "to_representation:",type(obj),obj
        return obj

    def to_internal_value(self, data):
        # 'data' should be a json structure
        # print "to_internal_value:",type(data),data
        return byteify(data)

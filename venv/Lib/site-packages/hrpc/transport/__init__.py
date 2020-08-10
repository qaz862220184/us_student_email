# coding=utf-8
__author__ = 'lxn3032'


import uuid

from collections import defaultdict


class Transport(object):
    def __init__(self, ep, rpc_client):
        super(Transport, self).__init__()
        self.endpoint = ep
        self.rpc_client = rpc_client
        self.session_id = str(uuid.uuid4())
        self._connected = False
        self._response_callbacks = defaultdict(set)

    def send(self, req):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def ping(self):
        raise NotImplementedError

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, v):
        self._connected = v

    def __del__(self):
        self.disconnect()

    def add_response_callback(self, reqid, cb):
        self._response_callbacks[reqid].add(cb)

    def pop_response_callback(self, reqid):
        return self._response_callbacks.pop(reqid, None)

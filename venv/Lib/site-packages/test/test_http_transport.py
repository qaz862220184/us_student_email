# coding=utf-8
__author__ = 'lxn3032'


import unittest

from hrpc.client import RpcClient
from hrpc.transport.http import HttpTransport


class MyClient(RpcClient):
    def initialize_transport(self):
        return HttpTransport('http://10.254.245.31:10081', self)


class TestHttpTansport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = MyClient(HttpTransport)

    def test_normal(self):
        poco = self.client.remote('poco-uiautomation-framework')
        print poco.get_screen_size()
        # test.ival = 2333
        # print test.ival
        # print test.array2[0]
        # print len(test.array1)
        # print len(test.array2)
        # print len(test.array3)


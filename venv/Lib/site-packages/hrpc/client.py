# coding=utf-8

import sys
import traceback
import threading
import uuid

from .object_proxy import RpcObjectProxy
from .exceptions import RpcException, RpcRemoteException, RpcTimeoutException, TransportDisconnected
from .utils.promise import Promise

__author__ = 'lxn3032'


class RpcClient(object):
    def __init__(self, auto_connect=True):
        self._timeout = 15
        self._resp_events = {}  # rpc request id -> threading.Event
        self._responses = {}  # reqid -> resp
        self._responses_mutex = threading.Lock()
        self._evaluated_count = 0
        self.transport = self.initialize_transport()

        if auto_connect:
            self.connect()

    def initialize_transport(self):
        raise NotImplementedError

    def connect(self):
        self.transport.connect()

    def disconnect(self):
        self.transport.disconnect()

    @property
    def connected(self):
        return bool(self.transport is not None and self.transport.connected)

    def remote(self, uri):
        return RpcObjectProxy(uri, self)

    def evaluate(self, obj_proxy, wait_for_response=True, out_response=None, on_response=None):
        # TODO: evaluate 的流程和response handling的流程要分离
        if not isinstance(obj_proxy, RpcObjectProxy):
            raise RuntimeError('Only RpcObjectProxy object can be evaluated. got {}'.format(repr(obj_proxy)))

        if not obj_proxy._evaluated__:
            self._evaluated_count += 1
            evt = threading.Event()
            if wait_for_response:
                reqid = str(uuid.uuid4())
                with self._responses_mutex:
                    self._resp_events[reqid] = evt
            else:
                reqid = ''

            # emit request
            if on_response:
                self.transport.add_response_callback(reqid, on_response)

            try:
                self.transport.send({'id': reqid, 'uri': obj_proxy._uri__, 'method': obj_proxy._invocation_path__})
            except TransportDisconnected as e:
                # 如果传输层断开了，则不需要析构该对象了
                obj_proxy._is_intermediate_uri__ = False
                raise

            if wait_for_response and not on_response:
                timedout = not evt.wait(timeout=self._timeout)
                if timedout:
                    raise RpcTimeoutException(self.transport.session_id, reqid, str(self.transport), obj_proxy._uri__,
                                              obj_proxy._invocation_path__, self._timeout)

                resp = self.get_response(reqid)
                if out_response is not None:
                    out_response.update(resp)
                if not resp:
                    raise RpcException(self.transport.session_id, reqid, 'Remote responses nothing!')
                if 'errors' in resp:
                    raise RpcRemoteException(resp)

                intermidiate_uri = resp.get('uri')
                if intermidiate_uri is not None:
                    obj_proxy._uri__ = intermidiate_uri
                    obj_proxy._invocation_path__ = ()
                    obj_proxy._is_intermediate_uri__ = True
                obj_proxy._evaluated__ = True
                obj_proxy._evaluated_value__ = resp.get('result')

        if obj_proxy._is_intermediate_uri__:
            return obj_proxy
        else:
            return obj_proxy._evaluated_value__

    def resolve(self, obj_proxy):
        @Promise
        def prom(resv, reject):
            def on_response(resp):
                # 因为是在另一个线程，所以不能直接raise，要把exception传到reject里
                try:
                    if not resp:
                        raise RpcException(self.transport.session_id, '', 'Remote responses nothing!')
                    if 'errors' in resp:
                        raise RpcRemoteException(resp)
                except Exception as e:
                    e.__tb__ = ''.join(traceback.format_exception(*sys.exc_info()))
                    reject(e)
                    return

                intermediate_uri = resp.get('uri')
                if intermediate_uri:
                    intermediate_obj = RpcObjectProxy(intermediate_uri, self)
                    intermediate_obj._evaluated__ = True
                    intermediate_obj._evaluated_value__ = resp.get('result')
                    intermediate_obj._is_intermediate_uri__ = True
                    resv(intermediate_obj)
                else:
                    resv(resp.get('result'))

            try:
                self.evaluate(obj_proxy, on_response=on_response)
            except RpcException as e:
                reject(e)

        return prom

    def invoke(self, object_proxy, method, args=()):
        @Promise
        def prom(resv, reject):
            def on_response(resp):
                # 因为是在另一个线程，所以不能直接raise，要把exception传到reject里
                try:
                    if not resp:
                        raise RpcException(self.transport.session_id, '', 'Remote responses nothing!')
                    if 'errors' in resp:
                        raise RpcRemoteException(resp)
                except Exception as e:
                    e.__tb__ = ''.join(traceback.format_exception(*sys.exc_info()))
                    reject(e)
                    return

                intermediate_uri = resp.get('uri')
                if intermediate_uri:
                    intermediate_obj = RpcObjectProxy(intermediate_uri, self)
                    intermediate_obj._evaluated__ = True
                    intermediate_obj._evaluated_value__ = resp.get('result')
                    intermediate_obj._is_intermediate_uri__ = True
                    resv(intermediate_obj)
                else:
                    resv(resp.get('result'))

            try:
                cache = []
                new_proxy = getattr(object_proxy, method).__call_no_evaluate__(cache, *args)
                self.evaluate(new_proxy, on_response=on_response)
            except RpcException as e:
                reject(e)

        return prom

    def put_response(self, resp):
        reqid = resp.get('id')
        if not reqid:
            # 忽略没有对应的请求id的响应，一般是服务端收到响应的提示信息而已
            return

        with self._responses_mutex:
            self._responses[reqid] = resp
            evt = self._resp_events.pop(reqid, None)
            if evt:
                evt.set()

    def get_response(self, reqid):
        with self._responses_mutex:
            return self._responses.pop(reqid, None)

    def reset_evaluation_counter(self):
        self._evaluated_count = 0

    def set_timeout(self, t):
        self._timeout = t

    def get_timeout(self):
        return self._timeout

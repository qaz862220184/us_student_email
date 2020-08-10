# coding=utf-8
__author__ = 'lxn3032'


import six


def simple_caster(cast_type):
    def func(self):
        val = self._client__.evaluate(self)
        if type(val) is RpcObjectProxy:
            val = val._evaluated_value__
        return cast_type(val)
    return func


def safe_repr(obj_proxy):
    return '{}/{}'.format(obj_proxy._uri__, obj_proxy._invocation_path__)


class RpcObjectProxy(object):
    """
    ensure immutable
    so that to keep evaluated value
    """

    reserved_slots = (
        '_uri__',
        '_client__',
        '_invocation_path__',
        '_evaluated__',
        '_evaluated_value__',
        '_is_intermediate_uri__',
        '_parent_ref__',
        '__call_no_evaluate__',
    )

    def __init__(self, uri, client, invocation_path=None, parent=None):
        self._uri__ = uri
        self._client__ = client
        self._invocation_path__ = invocation_path or ()
        self._evaluated__ = False
        self._evaluated_value__ = None
        self._is_intermediate_uri__ = False
        self._parent_ref__ = parent  # chain调用后保留parent的引用，以便在所有对象析构后，parent才请求远程析构

    # 链式调用代理
    def __getattr__(self, key):
        # 新调用链
        path = self._invocation_path__ + (('getattr', key), )
        new_obj = RpcObjectProxy(self._uri__, self._client__, path, self)
        return new_obj

    def __getitem__(self, item):
        path = self._invocation_path__ + (('getitem', item), )
        new_obj = RpcObjectProxy(self._uri__, self._client__, path, self)
        return new_obj

    def __len__(self):
        path = self._invocation_path__ + (('len', ()), )
        length = self._client__.evaluate(RpcObjectProxy(self._uri__, self._client__, path, self))
        return length

    def __iter__(self):
        if self._is_intermediate_uri__:
            # 这种写法目前只适用于远程list，远程dict还不行
            for i in range(len(self)):
                yield self[i]
        else:
            for v in self._client__.evaluate(self):
                yield v

    def __setattr__(self, key, value):
        if key in self.reserved_slots:
            self.__dict__[key] = value
        else:
            # 处理远程对象赋值给远程对象的情况
            is_intermediate = False
            if type(value) is RpcObjectProxy:
                value = self._client__.evaluate(value)
                if type(value) is RpcObjectProxy:
                    is_intermediate = value._is_intermediate_uri__
            if is_intermediate:
                path = self._invocation_path__ + (('=uri', (key, value._uri__)), )
            else:
                path = self._invocation_path__ + (('=', (key, value)), )
            self._client__.evaluate(RpcObjectProxy(self._uri__, self._client__, path, self))
        return value

    def __call__(self, *args):
        remote_obj_cache = []
        return self._client__.evaluate(self.__call_no_evaluate__(remote_obj_cache, *args))

    def __call_no_evaluate__(self, _cache, *args):
        # 执行call，但不对call进行立即求值，只对参数进行求值，并将是intermediate的参数保存到_cache中，以免远程释放
        calc_args = []
        for a in args:
            if type(a) is RpcObjectProxy:
                a = self._client__.evaluate(a)
                if type(a) is RpcObjectProxy and a._is_intermediate_uri__:
                    _cache.append(a)
                    calc_args.append(('uri', a._uri__))
                else:
                    calc_args.append(('', a))
            else:
                calc_args.append(('', a))
        path = self._invocation_path__ + (('call', tuple(calc_args)), )
        return RpcObjectProxy(self._uri__, self._client__, path, self)

    def __del__(self):
        # 代理对象析构时，请求远程对象也析构，并不需要等待返回
        if self._is_intermediate_uri__:
            action = (('del', ()), )
            self._client__.evaluate(RpcObjectProxy(self._uri__, self._client__, action), wait_for_response=False)

    # 类型转换导致求值
    def __str__(self):
        val = self._client__.evaluate(self)
        if type(val) is RpcObjectProxy:
            val = val._evaluated_value__
        if six.PY2 and isinstance(val, unicode):
            val = val.encode('utf-8')
        return str(val)

    if six.PY2:
        __unicode__ = simple_caster(unicode)
        __long__ = simple_caster(long)

    __repr__ = simple_caster(repr)
    __int__ = simple_caster(int)
    __float__ = simple_caster(float)
    __abs__ = simple_caster(abs)

    # calculation
    def __add__(self, other):
        return self._client__.evaluate(self) + other

    def __sub__(self, other):
        return self._client__.evaluate(self) - other

    def __mul__(self, other):
        return self._client__.evaluate(self) * other

    def __div__(self, other):
        return self._client__.evaluate(self) / other

    def __divmod__(self, other):
        raise NotImplementedError

    def __floordiv__(self, other):
        return self._client__.evaluate(self) // other

    def __pow__(self, power, modulo=None):
        return self._client__.evaluate(self) ** power

    def __radd__(self, other):
        return other + self._client__.evaluate(self)

    def __rsub__(self, other):
        return other - self._client__.evaluate(self)

    def __rmul__(self, other):
        return other * self._client__.evaluate(self)

    def __rdiv__(self, other):
        return other / self._client__.evaluate(self)

    # 运算并赋值
    # 使用兼容方式，自动展开成 obj = obj + xxx，并进入到赋值运算的拦截器
    # __iadd__, __isub__, __imul__, __idiv__

    # logic
    def __and__(self, other):
        return self._client__.evaluate(self) and other

    def __or__(self, other):
        return self._client__.evaluate(self) or other

    def __xor__(self, other):
        return bool(self._client__.evaluate(self)) != bool(other)

    def __rand__(self, other):
        return other and self._client__.evaluate(self)

    def __ror__(self, other):
        return other or self._client__.evaluate(self)

    def __rxor__(self, other):
        return bool(other) != bool(self._client__.evaluate(self))

    def __nonzero__(self):
        return bool(self._client__.evaluate(self))

    # inclusion
    def __contains__(self, item):
        return item in self._client__.evaluate(self)

    # comparison
    if six.PY2:
        def __cmp__(self, other):
            return cmp(self._client__.evaluate(self), other)

    def __eq__(self, other):
        return self._client__.evaluate(self) == other

    def __ge__(self, other):
        return self._client__.evaluate(self) >= other

    def __gt__(self, other):
        return self._client__.evaluate(self) > other

    def __le__(self, other):
        return self._client__.evaluate(self) <= other

    def __lt__(self, other):
        return self._client__.evaluate(self) < other

    def __ne__(self, other):
        return self._client__.evaluate(self) != other

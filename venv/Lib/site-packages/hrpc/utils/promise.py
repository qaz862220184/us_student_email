# coding=utf-8
__author__ = 'lxn3032'


import traceback
import inspect


__all__ = ['Promise']


def __raise(ex):
    if isinstance(ex, Exception):
        raise ex
    else:
        raise Exception(ex)


class Handler(object):
    def __init__(self, on_fulfilled, on_rejected):
        self.on_fulfilled = on_fulfilled
        self.on_rejected = on_rejected


class Promise(object):
    PENDING = 0
    FULFILLED = 1
    REJECTED = 2

    def __init__(self, fn):
        super(self.__class__, self).__init__()
        self.state = self.PENDING
        self.value = ()
        self.kwvalue = {}
        self.handlers = []
        self.__do_resolve(fn, self.__resolve, self.__reject)

    def then(self, on_fulfilled, on_rejected=None):
        def fn(resolve, reject):
            def resolver(*result, **kw):
                if callable(on_fulfilled):
                    try:
                        ret = on_fulfilled(*result, **kw)
                        if type(ret) is tuple:
                            return resolve(*ret)
                        else:
                            return resolve(ret)
                    except Exception as e:
                        traceback.print_exc()
                        e.__tb__ = traceback.format_exc()
                        return reject(e)
                else:
                    return resolve(*result, **kw)

            def rejector(*error, **kw):
                if callable(on_rejected):
                    try:
                        ret = on_rejected(*error, **kw)
                        if type(ret) is tuple:
                            return reject(*ret)
                        else:
                            return reject(ret)
                    except Exception as e:
                        traceback.print_exc()
                        e.__tb__ = traceback.format_exc()
                        return reject(e)
                else:
                    return reject(*error, **kw)

            self.done(resolver, rejector)

        return self.__class__(fn)

    def catch(self, on_rejected):
        return self.then(None, on_rejected)

    def final(self, cb):
        P = self.__class__
        return self.then(
            lambda v: P.resolve(cb()).then(lambda: v),
            lambda v: P.resolve(cb()).then(lambda: __raise(v))
        )

    def done(self, on_fulfilled=None, on_rejected=None):
        self.__handle(Handler(on_fulfilled, on_rejected))

    @staticmethod
    def resolve(*value, **kw):
        def fn(resolve, reject):
            resolve(*value, **kw)

        return Promise(fn)

    @staticmethod
    def reject(*value, **kw):
        def fn(resolve, reject):
            reject(*value, **kw)

        return Promise(fn)

    def __fulfill(self, *result, **kw):
        self.state = self.FULFILLED
        self.value = result
        self.kwvalue = kw
        for handler in self.handlers:
            self.__handle(handler)
        self.handlers = []

    def __reject(self, *error, **kw):
        self.state = self.REJECTED
        self.value = error
        self.kwvalue = kw
        for handler in self.handlers:
            self.__handle(handler)
        self.handlers = []

    def __resolve(self, *result, **kw):
        try:
            if len(result) > 0:
                then = self.__get_then(result[0])
                if then:
                    self.__do_resolve(then, self.__resolve, self.__reject)
                    return
            self.__fulfill(*result, **kw)
        except Exception as e:
            traceback.print_exc()
            e.__tb__ = traceback.format_exc()
            self.__reject(e)

    def __get_then(self, value):
        if hasattr(value, 'then') and callable(value.then):
            return value.then
        return None

    def __do_resolve(self, fn, on_fulfilled, on_rejected):
        try:
            def resolved(*value, **kw):
                if self.state != self.PENDING:
                    return
                on_fulfilled(*value, **kw)

            def rejected(*reason, **kw):
                if self.state != self.PENDING:
                    return
                on_rejected(*reason, **kw)

            args_count = len(inspect.getargspec(fn)[0])
            if args_count == 1:
                fn(resolved)
            else:
                fn(resolved, rejected)
        except Exception as e:
            if self.state != self.PENDING:
                return
            traceback.print_exc()
            e.__tb__ = traceback.format_exc()
            on_rejected(e)

    def __handle(self, handler):
        if self.state == self.PENDING:
            self.handlers.append(handler)
        else:
            if self.state == self.FULFILLED and callable(handler.on_fulfilled):
                handler.on_fulfilled(*self.value, **self.kwvalue)
            elif self.state == self.REJECTED and callable(handler.on_rejected):
                handler.on_rejected(*self.value, **self.kwvalue)

from inspect import getargspec


__version__ = '0.1.0'


class Value(object):

    def __new__(class_, *args, **kwargs):
        self = object.__new__(class_, *args, **kwargs)
        para, varargs, keywords, defaults = getargspec(self.__init__)
        if varargs:
            raise ValueError('`*args` are not allowed in __init__')
        if keywords:
            raise ValueError('`**kwargs` are not allowed in __init__')
        if not all(type(p) is str for p in para):
            raise ValueError('parameter unpacking is not allowed in __init__')
        defaults = () if not defaults else defaults
        params = dict(zip(para[:0:-1], defaults[::-1]))
        params.update(dict(zip(para[1:], args) + kwargs.items()))
        self.__params = params

        def setprop(key):
            setattr(class_, key, property(lambda x: x.__params[key]))

        for k in params:
            setprop(k)
        return self

    def __repr__(self):
        null = object()
        para, _, _, defaults = getargspec(self.__init__)
        para = para[1:]
        actuals = [getattr(self, p) for p in para]
        defaults = () if not defaults else defaults
        defaults = defaults[1:] if len(defaults) == len(para) + 1 else defaults
        defaults = (null,) * (len(para) - len(defaults)) + defaults
        return '%s(%s)' % (self.__class__.__name__,
                ', '.join(repr(a) for a, d in zip(actuals, defaults) if a != d))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __ne__(self, other):
        return repr(self) != repr(other)

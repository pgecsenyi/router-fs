from types import FunctionType


def decorate_all(decorator):

    class DecorateAll(type):

        def __new__(cls, name, bases, dct):
            for attr, value in dct.items():
                if do_decorate(attr, value):
                    dct[attr] = decorator(value)

            return super(DecorateAll, cls).__new__(cls, name, bases, dct)

        def __setattr__(cls, attr, value):
            if do_decorate(attr, value):
                value = decorator(value)
            super(DecorateAll, cls).__setattr__(attr, value)

    return DecorateAll


def do_decorate(attr, value):
    return (
        '__' not in attr and
        isinstance(value, FunctionType) and
        getattr(value, 'decorate', True))


def dont_decorate(func):
    func.decorate = False
    return func

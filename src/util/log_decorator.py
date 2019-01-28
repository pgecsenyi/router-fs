import functools
import logging


def log_decorator(func):

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        class_name = type(self).__name__
        func_name = func.__name__
        positional_arg_strings = [str(a) for a in args]
        named_args = [str(a) for a in kwargs]
        all_args = ','.join(positional_arg_strings + named_args)

        logging.log(logging.INFO, '%s.%s(%s)', class_name, func_name, all_args)

        try:
            return_value = func(self, *args, **kwargs)
            logging.log(logging.INFO, '    -> %s', return_value)
        except Exception as ex:
            logging.log(logging.INFO, '    raised %s', str(ex))
            raise

        return return_value

    return wrapper

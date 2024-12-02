from Error_Handler.Logger import Logger


logger = Logger('error_logs',
                './Logs/error.log',
                '%(asctime)s %(levelname)s. %(message)s')


def catch_exceptions(cls):  # decorator for catching all exceptions from functions inside the class
    class CatchExceptionClass:
        def __init__(self, *args, **kwargs):
            self.ins = cls(*args, **kwargs)

        def __getattribute__(self, name):
            try:
                x = super().__getattribute__(name)
                return x
            except AttributeError:
                pass

            origin_attr = self.ins.__getattribute__(name)
            if callable(origin_attr):
                def method(*args, **kwargs):
                    try:
                        return origin_attr(*args, **kwargs)
                    except Exception as e:
                        logger.write_log(level=20,
                                         message=f"An exception caught in {cls.__name__}.{name}: {e}")
                return method
            else:
                return origin_attr

    return CatchExceptionClass

from time import time
from .сreational_patterns import Logger


class FrameRoute:

    def __init__(self, routes: dict, url: str):
        self.routes = routes
        self.url = url

    # Декоратор. При вызове обновляет словарь маршрутов.
    def __call__(self, cls):
        self.routes[self.url] = cls()


class FrameDebug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def time_decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time()
                func_result = func(*args, **kwargs)
                end_time = time()
                time_interval = end_time - start_time

                Logger.log(f" Debug >>> {self.name} выполнялась {time_interval:2.3f} ms")

                return func_result

            return wrapper
        return time_decorator(cls)
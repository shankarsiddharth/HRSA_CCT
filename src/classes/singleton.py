import threading

from app_debug.app_debug import IS_DEBUG_MODE_ENABLED


class Singleton(type):
    _instances: dict = dict()
    _instance_locks: dict = dict()

    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instance_locks:
                cls._instance_locks[cls] = threading.Lock()

        with cls._instance_locks[cls]:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
                if IS_DEBUG_MODE_ENABLED:
                    print("{}.__init__() : Singleton.__call__()".format(cls.__name__))
        return cls._instances[cls]

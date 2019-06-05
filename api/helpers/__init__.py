import hashlib


def md5_string(str):
    m = hashlib.md5(str.encode('utf-8'))
    return m.hexdigest()


class Singleton:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

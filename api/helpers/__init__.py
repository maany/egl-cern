import hashlib


def md5_string(str):
    m = hashlib.md5(str.encode('utf-8'))
    return m.hexdigest()

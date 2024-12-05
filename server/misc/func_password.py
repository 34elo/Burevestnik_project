import hashlib
from server.settings import HASH_SALT


def my_hash(password):
    password = str(password) + HASH_SALT
    hash_password = hashlib.md5(password.encode()).hexdigest()
    return hash_password


def f():
    print("hello, world")  # пасхалка

from threading import Lock

from cachetools import TTLCache

_store = TTLCache(maxsize=1000, ttl=1 * 60 * 60)
_current_id = [1]
_max_id = 1000

_lock = Lock()


def _get_msg_id():
    """
    Get an available message id.

    :return: message if as an int
    """
    _lock.acquire()
    msg_id = _current_id[0]
    _current_id[0] = _current_id[0] % _max_id + 1
    _lock.release()
    return msg_id


def save(ctx_msg):
    """
    Save a context message.

    :param ctx_msg: context message
    :return: message id as an int
    """
    msg_id = _get_msg_id()
    _store[msg_id] = ctx_msg
    return msg_id


def find(msg_id: int):
    """
    Find a context message.

    :param msg_id: message id as an int
    :return: context message
    """
    return _store.get(msg_id)

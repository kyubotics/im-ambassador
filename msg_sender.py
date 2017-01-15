import os
import sys
import importlib

from little_shit import get_msg_senders_dir

_senders = {}


def as_sender(via):
    def decorator(func):
        _senders[via] = func
        return func

    return decorator


def _load_senders():
    mod_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(get_msg_senders_dir())
    )
    mods = [os.path.splitext(file)[0] for file in mod_files]
    for mod_name in mods:
        importlib.import_module('msg_senders.' + mod_name)


_load_senders()


def send_message(target: dict, content):
    sender = _senders.get(target.get('via', ''))
    if sender:
        sender(target, content)
    else:
        print('Unsupported message platform:', target.get('via'), file=sys.stderr)

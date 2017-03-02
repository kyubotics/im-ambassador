import os
import json
import importlib


class SkipException(Exception):
    pass


def _mkdir_if_not_exists_and_return_path(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_root_dir():
    return os.path.split(os.path.realpath(__file__))[0]


def get_plugin_dir(plugin_dir_name):
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), plugin_dir_name))


def load_plugins(plugin_dir_name, module_callback=None):
    plugin_dir = get_plugin_dir(plugin_dir_name)
    plugin_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(plugin_dir)
    )
    plugins = [os.path.splitext(file)[0] for file in plugin_files]
    for mod_name in plugins:
        mod = importlib.import_module(plugin_dir_name + '.' + mod_name)
        if module_callback:
            module_callback(mod)


def get_db_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'db'))


def get_default_db_path():
    return os.path.join(get_db_dir(), 'default.sqlite')


def get_tmp_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'tmp'))


def get_config():
    config = {}
    json_path = os.path.join(get_root_dir(), 'config.json')
    py_path = os.path.join(get_root_dir(), 'config.py')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            config = json.load(f)
    elif os.path.exists(py_path):
        mod = importlib.import_module('config')
        if hasattr(mod, 'config'):
            config = mod.config.copy()
    return config


def get_msg_src_list():
    src = get_config().get('src', [])
    for s in src:
        for r in s.get('rules', []):
            r['id'] = r.get('id', 'default')
            for k in ('type', 'group', 'group_id', 'discuss', 'discuss_id', 'sender', 'sender_id', 'keywords'):
                if k in r and isinstance(r[k], str):
                    r[k] = [r[k]]
                k = '!' + k
                if k in r and isinstance(r[k], str):
                    r[k] = [r[k]]
    return src


def get_msg_dst_list():
    dst = get_config().get('dst', [])
    for d in dst:
        for r in d.get('rules', []):
            r['id'] = r.get('id', 'default')
    return dst

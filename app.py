import os
import sys
import importlib

from flask import Flask, request

from little_shit import SkipException, get_filters_dir
from filter import apply_filters

app = Flask(__name__)


@app.route('/qq/', methods=['POST'])
def _handle_qq_message():
    ctx_msg = request.json
    ctx_msg['via'] = 'qq'
    return _main(ctx_msg)


@app.route('/wx/', methods=['POST'])
def _handle_wx_src_message():
    ctx_msg = request.json
    ctx_msg['via'] = 'wx'
    return _main(ctx_msg)


@app.route('/wx/<string:account>', methods=['POST'])
def _handle_wx_account_message(account):
    ctx_msg = request.json
    ctx_msg['via'] = 'wx'
    ctx_msg['receiver_account'] = account
    return _main(ctx_msg)


def _main(ctx_msg: dict):
    try:
        if ctx_msg.get('post_type') != 'receive_message':
            raise SkipException
        if not apply_filters(ctx_msg):
            raise SkipException
    except SkipException:
        # Skip this message
        pass

    return '', 204


def _load_filters():
    filter_mod_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(get_filters_dir())
    )
    command_mods = [os.path.splitext(file)[0] for file in filter_mod_files]
    for mod_name in command_mods:
        importlib.import_module('filters.' + mod_name)


if __name__ == '__main__':
    _load_filters()
    host = os.environ.get('IM_AMBASSADOR_HOST', '0.0.0.0')
    port = os.environ.get('IM_AMBASSADOR_PORT', '8080')
    if len(sys.argv) == 3:
        host, port = sys.argv[1:]
    elif len(sys.argv) == 2:
        port = sys.argv[1]
    app.run(host=host, port=port)

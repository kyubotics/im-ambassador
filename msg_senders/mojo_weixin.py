import requests

from msg_sender import as_sender


@as_sender(via='wx')
def send_message(target: dict, content: str):
    msg_type = target.get('type', 'friend')
    if msg_type == 'group':
        return send_group_message(target, content)
    elif msg_type == 'friend':
        return send_friend_message(target, content)


def send_group_message(target: dict, content: str):
    api_url = target.get('api_url', '').rstrip('/')
    if not api_url:
        return

    params_list = []
    if target.get('group_id'):
        params_list.append({'id': target.get('group_id')})
    elif target.get('group'):
        params_list.append({'displayname': target.get('group')})

    for params in params_list:
        params['content'] = content
        requests.get(api_url + '/send_group_message', params=params)


def send_friend_message(target: dict, content: str):
    api_url = target.get('api_url', '').rstrip('/')
    if not api_url:
        return

    params_list = []
    if target.get('friend_account'):
        params_list.append({'account': target.get('friend_account')})
    elif target.get('friend_id'):
        params_list.append({'id': target.get('friend_id')})
    elif target.get('friend'):
        params_list.append({'displayname': target.get('friend')})

    for params in params_list:
        params['content'] = content
        requests.get(api_url + '/send_friend_message', params=params)

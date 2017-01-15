import requests

from msg_sender import as_sender


@as_sender(via='qq')
def send_message(target: dict, content: str):
    msg_type = target.get('type', 'friend')
    if msg_type == 'group':
        return send_group_message(target, content)
    elif msg_type == 'discuss':
        return send_discuss_message(target, content)
    elif msg_type == 'friend':
        return send_friend_message(target, content)


def send_group_message(target: dict, content: str):
    api_url = target.get('api_url', '').rstrip('/')
    if not api_url:
        return

    params_list = []
    if target.get('group_uid'):
        params_list.append({'uid': target.get('group_uid')})
    elif target.get('group_id'):
        params_list.append({'id': target.get('group_id')})
    elif target.get('group'):
        group_name = target.get('group')
        group_list = requests.get(api_url + '/get_group_basic_info').json()
        group_list = list(filter(lambda g: g.get('name') == group_name, group_list)) if group_list else group_list
        if not group_list:
            # 没有找到群组名符合的群组
            return
        params_list = list(map(lambda g: {'id': g.get('id')}, group_list))

    for params in params_list:
        params['content'] = content
        requests.get(api_url + '/send_group_message', params=params)


def send_discuss_message(target: dict, content: str):
    api_url = target.get('api_url', '').rstrip('/')
    if not api_url:
        return

    params_list = []
    if target.get('discuss_id'):
        params_list.append({'id': target.get('discuss_id')})
    elif target.get('discuss'):
        discuss_name = target.get('discuss')
        discuss_list = requests.get(api_url + '/get_discuss_info').json()
        discuss_list = list(filter(
            lambda g: g.get('name') == discuss_name,
            discuss_list
        )) if discuss_list else discuss_list
        if not discuss_list:
            # 没有找到讨论组名符合的讨论组
            return
        params_list = list(map(lambda d: {'id': d.get('id')}, discuss_list))

    for params in params_list:
        params['content'] = content
        requests.get(api_url + '/send_discuss_message', params=params)


def send_friend_message(target: dict, content: str):
    api_url = target.get('api_url', '').rstrip('/')
    if not api_url:
        return

    params_list = []
    if target.get('friend_account') or target.get('friend_uid'):
        params_list.append({'uid': target.get('friend_account') or target.get('friend_uid')})
    elif target.get('friend_id'):
        params_list.append({'id': target.get('friend_id')})
    elif target.get('friend'):
        friend_name = target.get('friend')
        friend_list = requests.get(api_url + '/get_friend_info').json()
        friend_list = list(filter(
            lambda g: g.get('name') == friend_name,
            friend_list
        )) if friend_list else friend_list
        if not friend_list:
            # 没有找到昵称符合的好友
            return
        params_list = list(map(lambda g: {'id': g.get('id')}, friend_list))

    for params in params_list:
        params['content'] = content
        requests.get(api_url + '/send_friend_message', params=params)

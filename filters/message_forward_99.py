import threading

from filter import as_filter
from little_shit import get_msg_dst_list, get_config
from msg_src_adapter import get_adapter_by_config

_dst = get_msg_dst_list()
_config = get_config()


@as_filter(priority=99)
def _filter(ctx_msg):
    if ctx_msg.get('ima_state') != 'received':
        return

    content = (ctx_msg.get('src_displayname') + '|') if ctx_msg.get('src_displayname') else ''
    content += ctx_msg.get('sender') or ctx_msg.get('sender_name') or ctx_msg.get('sender_id') or '未知用户'
    if ctx_msg.get('msg_type') == 'group':
        content += '@' + (ctx_msg.get('group') or ctx_msg.get('group_id') or '未知群组')
    if ctx_msg.get('msg_type') == 'discuss':
        content += '@' + (ctx_msg.get('discuss') or ctx_msg.get('discuss_id') or '未知讨论组')
    content += ': ' + ctx_msg.get('content', '')

    for d in _dst:
        for rule in d.get('rules', []):
            if rule['id'] == ctx_msg.get('rule_id'):
                target = {'rule_id': rule['id'], 'dst_config': {}}
                for k in d.keys():
                    if k != 'rules':
                        # 把该 dst 的除 rules 的字段都复制到 target，通常包括 via、api_url
                        target['dst_config'][k] = d[k]
                for k in rule.keys():
                    if k != 'id':
                        # 把该 rule 的除 id 的字段都复制到 target，通常包括 msg_type，user_id 等
                        target[k] = rule[k]

                if target.get('allow_reply') or _config.get('allow_reply'):
                    final_content = '#' + str(ctx_msg['msg_id']) + ' ' + content
                else:
                    final_content = content

                threading.Thread(target=get_adapter_by_config(target['dst_config']).send_message,
                                 args=(target, final_content)).start()

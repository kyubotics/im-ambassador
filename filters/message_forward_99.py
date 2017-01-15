import threading

import msg_sender
from filter import as_filter
from little_shit import get_msg_dst_list

_dst = get_msg_dst_list()


@as_filter(priority=99)
def _filter(ctx_msg):
    content = '#' + str(ctx_msg['msg_id']) + ' ' \
              + ((ctx_msg.get('src_displayname') + '|') if ctx_msg.get('src_displayname') else '') \
              + ctx_msg.get('sender', '') \
              + (('@' + ctx_msg.get('group')) if ctx_msg.get('type') == 'group_message' else '') \
              + (('@' + ctx_msg.get('discuss')) if ctx_msg.get('type') == 'discuss_message' else '') \
              + ': ' + ctx_msg.get('content')

    for d in _dst:
        for rule in d.get('rules', []):
            if rule['id'] == ctx_msg.get('rule_id'):
                target = {'rule_id': rule['id']}
                for k in d.keys():
                    if k != 'rules':
                        # 把该 dst 的除 rules 的字段都复制到 target，通常包括 via、api_url
                        target[k] = d[k]
                for k in rule.keys():
                    if k != 'id':
                        # 把该 rule 的除 id 的字段都复制到 target，通常包括 type，receiver_account 等
                        target[k] = rule[k]
                threading.Thread(target=msg_sender.send_message, args=(target, content)).start()

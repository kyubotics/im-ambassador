import re

import msg_store
from filter import as_filter
from little_shit import get_msg_src_list

_src = get_msg_src_list()


@as_filter(priority=100)
def _filter(ctx_msg):
    for s in _src:
        if s.get('via') == ctx_msg.get('via') and s.get('account') == ctx_msg.get('receiver_account'):
            matched_src = s
            break
    else:
        return False

    should_forward = False
    if not matched_src.get('rules'):
        # rules 为空
        ctx_msg['rule_id'] = 'default'
        should_forward = True
    else:
        # 尝试匹配规则
        for r in matched_src['rules']:
            match = True
            rule = r.copy()
            rule_id = rule['id']
            del rule['id']

            # 尝试匹配消息类型
            if 'type' in rule:
                if rule['type'] != ctx_msg.get('msg_type'):
                    # 消息类型不匹配
                    match = False
                del rule['type']

            # 尝试匹配群组名、发送者账号等
            for key in ('group', 'group_uid', 'discuss', 'sender', 'sender_account'):
                if key in rule:
                    if ctx_msg.get(key) not in rule[key]:
                        match = False
                    del rule[key]

            # 尝试匹配消息关键词
            if 'keywords' in rule:
                for kw in rule['keywords']:
                    if kw in ctx_msg.get('content', ''):
                        break
                else:
                    # 关键词不匹配
                    match = False
                del rule['keywords']

            # 尝试匹配正则
            if 'pattern' in rule:
                m = re.match(rule['pattern'], ctx_msg.get('content', ''))
                if m:
                    content = m.group('content')
                    if content:
                        ctx_msg['content'] = content
                else:
                    # 关键词不匹配
                    match = False
                del rule['pattern']

            # 尝试匹配其它自定义字段
            for k, v in rule.items():
                if v != ctx_msg.get(k):
                    match = False

            if match:
                # 匹配到一个规则，跳出循环
                ctx_msg['rule_id'] = rule_id
                should_forward = True
                break

    if should_forward:
        # 消息来源规则匹配成功，该消息需要转发
        for k in matched_src.keys():
            if k not in ('via', 'account', 'rules'):
                # 把该 src 除了 via、account、rules 的其它自定义字段复制到 ctx_msg，通常包括 api_url
                ctx_msg[k] = matched_src[k]
        ctx_msg['msg_id'] = msg_store.save(ctx_msg)
        return True
    return False

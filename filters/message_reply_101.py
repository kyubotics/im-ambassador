import re
import threading

import msg_store
import msg_sender
from filter import as_filter
from little_shit import get_msg_dst_list, get_config

_dst = get_msg_dst_list()
_config = get_config()


@as_filter(priority=101)
def _filter(ctx_msg):
    g_allow_reply = _config.get('allow_reply', False)
    g_reply_pattern = _config.get('reply_pattern', '')
    g_reply_format = _config.get('reply_format', '{{reply}}')

    for d in _dst:
        if d.get('via') != ctx_msg.get('via'):
            continue

        for rule in d.get('rules', []):
            allow_reply = rule.get('allow_reply') or g_allow_reply
            reply_pattern = rule.get('reply_pattern') or g_reply_pattern
            reply_format = rule.get('reply_format') or g_reply_format

            if not allow_reply or not reply_pattern:
                # 这个规则不允许回复，或没有设置回复匹配正则
                continue

            # 尝试匹配消息类型
            if 'type' in rule:
                if rule['type'] != ctx_msg.get('msg_type'):
                    # 消息类型不匹配
                    continue

            # 尝试匹配群组名、发送者账号等
            match = True  # 表示这条规则的群组名、账号等是否匹配
            valid = False  # 表示这条规则是否有效（如果没有设置任何群组名、账号等，那就不应该认为匹配到了
            for k1, k2 in (('group', 'group'), ('group_uid', 'group_uid'), ('discuss', 'discuss'),
                           ('sender', 'friend'), ('sender_account', 'friend_account')):
                # k1 对应 ctx_msg 中的键，k2 对应 rule 中的键
                if k1 in ctx_msg and k2 in rule:
                    valid = True
                    if ctx_msg[k1] != rule[k2]:
                        match = False
                        break
            if not valid or not match:
                # 群组名、发送者账号等不匹配
                continue

            # 尝试使用 reply_pattern 从消息内容中匹配出要回复的消息 ID 和回复内容
            m = re.match(reply_pattern, ctx_msg.get('content', ''))
            if not m:
                # 正则匹配失败
                continue
            msg_id = m.group('id')
            reply_content = m.group('reply')
            if not msg_id or not msg_id.isdigit() or not reply_content:
                # 正则没有匹配出消息 ID 和回复内容
                continue

            # 尝试检查消息中匹配出来的 msg_id 对应的消息的 rule_id 是否和当前 rule 的 id 相同
            ctx_msg = msg_store.find(int(msg_id))
            if not ctx_msg or ctx_msg.get('rule_id') != rule['id']:
                continue

            # 到这还没有跳出，说明这条消息确实是在回复获取到的这个 ctx_msg，因此发送回复消息
            content = re.sub('\{\{\s*reply\s*\}\}', reply_content, reply_format)

            target = ctx_msg.copy()
            target['type'] = target.get('msg_type')
            for k in ('sender', 'sender_id', 'sender_uid', 'sender_account'):
                if k in ctx_msg:
                    # 把原 ctx_msg 中的所有 sender 相关的字段改成 friend，放到 target，以便 msg_sender 发送
                    target[k.replace('sender', 'friend')] = ctx_msg[k]

            threading.Thread(target=msg_sender.send_message, args=(target, content)).start()
            ctx_msg['ima_state'] = 'replied'  # 已当做回复消息处理，标记状态为 replied
            return  # 回复之后需要立即返回，终止循环的剩余部分

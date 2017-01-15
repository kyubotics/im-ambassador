import msg_sender
from filter import as_filter
from config import config

dst = config['dst']

for d in dst:
    for r in d.get('rules', []):
        r['id'] = r.get('id', 'default')


@as_filter(priority=99)
def _filter(ctx_msg):
    content = ((ctx_msg.get('src_displayname') + '|') if ctx_msg.get('src_displayname') else '') \
              + ctx_msg.get('sender', '') \
              + (('@' + ctx_msg.get('group')) if ctx_msg.get('type') == 'group_message' else '') \
              + (('@' + ctx_msg.get('discuss')) if ctx_msg.get('type') == 'discuss_message' else '') \
              + ': ' + ctx_msg.get('content')
    print('需要转发的内容:', content)

    for d in dst:
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
                print('即将发送到:', target)
                msg_sender.send_message(target, content)

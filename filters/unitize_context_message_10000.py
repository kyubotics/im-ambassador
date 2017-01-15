"""
This filter unitize context messages from different platform.
"""

from filter import as_filter


@as_filter(priority=10000)
def _unitize(ctx_msg):
    for k in ('id', 'sender_id', 'sender_uid', 'receiver_id', 'receiver_uid',
              'group_id', 'group_uid', 'discuss_id', 'discuss_uid'):
        if k in ctx_msg:
            ctx_msg[k] = str(ctx_msg[k])

    ctx_msg['msg_type'] = ctx_msg.get('type', '').split('_')[0]

    if ctx_msg.get('via') == 'qq':
        ctx_msg['sender_account'] = ctx_msg.get('sender_uid')
        ctx_msg['receiver_account'] = ctx_msg.get('receiver_uid')

        if not ctx_msg.get('format'):
            # All QQ messages that can be received are text
            ctx_msg['format'] = 'text'

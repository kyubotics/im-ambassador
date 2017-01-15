"""
This filter intercepts messages that contains content not allowed.
"""

from filter import as_filter


@as_filter(priority=999)
def _filter(ctx_msg):
    return ctx_msg.get('post_type') == 'receive_message' \
           and ctx_msg.get('msg_type') in ('friend', 'group', 'discuss')

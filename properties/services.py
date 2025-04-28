from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_udate(post_id):
    print('post :',post_id)
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        # f"post_{post_id}",
        "properties",
        {
            "type":"update_event",
            "data":"faiz"
        }

    )
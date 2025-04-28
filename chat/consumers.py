import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message, Conversation, UserStatus
from django.utils import timezone
import base64
from django.core.files.base import ContentFile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.update_user_status(True)
            await self.channel_layer.group_add(
                f"user_{self.user.id}",
                self.channel_name
            )

    async def disconnect(self, close_code):
        if hasattr(self, 'user') and self.user.is_authenticated:
            await self.update_user_status(False)
            await self.channel_layer.group_discard(
                f"user_{self.user.id}",
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'chat_message')

        if message_type == 'typing_status':
            await self.handle_typing_status(data)
        elif message_type == 'chat_message':
            await self.handle_chat_message(data)
        elif message_type == 'delete_message':
            await self.handle_delete_message(data)
        elif message_type == 'mark_read':
            await self.handle_mark_read(data)

    async def handle_typing_status(self, data):
        conversation_id = data.get('conversation_id')
        is_typing = data.get('is_typing', False)
        
        await self.update_typing_status(conversation_id, is_typing)
        
        # Notify other user
        conversation = await self.get_conversation(conversation_id)
        other_user = await self.get_other_user(conversation)
        
        await self.channel_layer.group_send(
            f"user_{other_user.id}",
            {
                "type": "typing_notification",
                "user_id": self.user.id,
                "is_typing": is_typing,
                "conversation_id": conversation_id
            }
        )

    async def handle_chat_message(self, data):
        message = await self.save_message(data)
        conversation = message.conversation
        other_user = await self.get_other_user(conversation)

        # إرسال الرسالة للمستخدم الآخر
        await self.channel_layer.group_send(
            f"user_{other_user.id}",
            {
                'type': 'chat_message',
                'message': await self.message_to_json(message)
            }
        )

        # إرسال الرسالة للمرسل
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': await self.message_to_json(message)
        }))

        # إرسال تحديث للمحادثات
        await self.send_chat_update(self.user.id)
        await self.send_chat_update(other_user.id)

    async def handle_delete_message(self, data):
        message_id = data.get('message_id')
        if message_id:
            message = await self.get_message(message_id)
            if message and message.sender == self.user:
                await self.delete_message(message_id)
                
                # إرسال إشعار الحذف لجميع المشاركين في المحادثة
                conversation = message.conversation
                for participant in await self.get_conversation_participants(conversation):
                    await self.channel_layer.group_send(
                        f"user_{participant.id}",
                        {
                            "type": "message_deleted",
                            "message": {
                                "message_id": str(message_id)  # تحويل إلى نص
                            }
                        }
                    )

    async def handle_mark_read(self, data):
        conversation_id = data.get('conversation_id')
        if conversation_id:
            await self.mark_messages_as_read(conversation_id)
            conversation = await self.get_conversation(conversation_id)
            other_user = await self.get_other_user(conversation)
            
            await self.channel_layer.group_send(
                f"user_{other_user.id}",
                {
                    "type": "messages_read",
                    "conversation_id": conversation_id,
                    "reader_id": self.user.id
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing_notification(self, event):
        await self.send(text_data=json.dumps(event))

    async def message_deleted(self, event):
        """إرسال إشعار حذف الرسالة للعميل"""
        await self.send(text_data=json.dumps({
            'type': 'message_deleted',
            'message': event['message']
        }))

    async def messages_read(self, event):
        await self.send(text_data=json.dumps(event))

    async def send_chat_update(self, user_id):
        """إرسال تحديث للمحادثات"""
        await self.channel_layer.group_send(
            f"user_{user_id}",
            {
                'type': 'chat_update',
                'message': {
                    'type': 'chat_update'
                }
            }
        )

    async def chat_update(self, event):
        """إرسال تحديث المحادثات للعميل"""
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def update_user_status(self, is_online):
        UserStatus.objects.update_or_create(
            user=self.user,
            defaults={'is_online': is_online, 'last_seen': timezone.now()}
        )

    @database_sync_to_async
    def update_typing_status(self, conversation_id, is_typing):
        status, _ = UserStatus.objects.get_or_create(user=self.user)
        status.is_typing = is_typing
        status.typing_in_conversation_id = conversation_id if is_typing else None
        status.save()

    @database_sync_to_async
    def get_or_create_conversation(self, recipient_id):
        recipient = User.objects.get(id=recipient_id)
        conversation = Conversation.objects.filter(
            participants=self.user
        ).filter(
            participants=recipient
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(self.user, recipient)
            
        return conversation

    @database_sync_to_async
    def create_message(self, conversation, content='', image_data=None):
        message = Message(
            conversation=conversation,
            sender=self.user,
            receiver=conversation.participants.exclude(id=self.user.id).first(),
            content=content
        )
        
        if image_data:
            # Convert base64 to image file
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_content = ContentFile(base64.b64decode(imgstr), name=f'msg_{conversation.id}_{timezone.now().timestamp()}.{ext}')
            message.image = image_content
            
        message.save()
        return message

    @database_sync_to_async
    def delete_message(self, message_id):
        try:
            message = Message.objects.get(id=message_id, sender=self.user)
            message.is_deleted = True
            message.save()
            return True
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def mark_messages_as_read(self, conversation_id):
        Message.objects.filter(
            conversation_id=conversation_id,
            receiver=self.user,
            is_read=False
        ).update(is_read=True)

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        return Conversation.objects.get(id=conversation_id)

    @database_sync_to_async
    def get_message(self, message_id):
        try:
            return Message.objects.select_related('conversation', 'sender').get(id=message_id)
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def get_other_user(self, conversation):
        return conversation.participants.exclude(id=self.user.id).first()

    @database_sync_to_async
    def save_message(self, data):
        recipient_id = data.get('recipient_id')
        if not recipient_id:
            raise ValueError('recipient_id is required')
            
        conversation = self.get_or_create_conversation_sync(recipient_id)
        content = data.get('message', '')
        image_data = data.get('image')
        
        message = Message.objects.create(
            conversation=conversation,
            sender=self.user,
            receiver=User.objects.get(id=recipient_id),
            content=content
        )
        
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_content = ContentFile(base64.b64decode(imgstr), name=f'msg_{conversation.id}_{timezone.now().timestamp()}.{ext}')
            message.image = image_content
            message.save()
            
        return message

    def get_or_create_conversation_sync(self, recipient_id):
        recipient = User.objects.get(id=recipient_id)
        conversation = Conversation.objects.filter(
            participants=self.user
        ).filter(
            participants=recipient
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(self.user, recipient)
            
        return conversation

    @database_sync_to_async
    def message_to_json(self, message):
        return {
            'id': message.id,
            'sender_id': message.sender.id,
            'content': message.content,
            'image': message.image.url if message.image else None,
            'created_at': message.created_at.isoformat(),
            'is_read': message.is_read
        }

    @database_sync_to_async
    def get_conversation_participants(self, conversation):
        return list(conversation.participants.all())

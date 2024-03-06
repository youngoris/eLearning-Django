from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatRoom, Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = self.room_name.replace(" ", "_")
        self.room_group_name = 'chat_%s' % self.room_name

        # 异步确保聊天室存在
        self.room, created = await self.get_room()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 处理接收到的消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].username  # 获取用户名

        # 发送消息到WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username  # 添加用户名
            }
        )

    # 接收到消息后的处理
    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # 获取用户名

        # 发送消息和用户名
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
        
    @database_sync_to_async
    def save_message(self, room_name, user, message):
        room = ChatRoom.objects.get(title=room_name)
        Message.objects.create(room=room, user=user, message=message)

    @database_sync_to_async
    def get_room(self):
        return ChatRoom.objects.get_or_create(title=self.room_name)
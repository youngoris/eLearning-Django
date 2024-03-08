from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from datetime import datetime
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # every user is in the same global chat room
        self.room_group_name = 'global_chat'
        
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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].real_name if self.scope["user"].real_name else self.scope["user"].username
        avatar = self.scope["user"].avatar.url if self.scope["user"].avatar else "static('admin/img/avatar.svg')"

        # current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'avatar': avatar,
                'timestamp': timestamp
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    

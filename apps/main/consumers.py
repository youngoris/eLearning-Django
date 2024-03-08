# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # 由于我们没有房间逻辑，这里不需要执行任何操作

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].username

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'avatar': self.scope["user"].avatar.url if self.scope["user"].avatar else "",
            'timestamp': "Now"  # 这里可以根据实际需要格式化时间戳
        }))

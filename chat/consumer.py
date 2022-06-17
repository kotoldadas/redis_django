import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"connected user => {self.scope['user']}")
        self.user: CustomUser = self.scope["user"]
        self.user.channel_name = self.channel_name
        await sync_to_async(self.user.save)()
        print(f"users new channel name => {self.user.channel_name}")

        self.room_name = "test_room"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # type: ignore

        await self.accept()

    async def disconnect(self, code):
        self.user.channel_name = None  # type: ignore
        await sync_to_async(self.user.save)()
        print(f"users new channel name => {self.user.channel_name}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)  # type: ignore

    async def receive(self, text_data, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(  # type: ignore
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        """it is called when any group message which type propery is 'chat_message' is received"""
        message = event["message"]

        # send message to websocket

        await self.send(text_data=json.dumps({"message": message}))

    async def success_message(self, event):

        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

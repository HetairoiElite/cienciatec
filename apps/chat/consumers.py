if __name__ == '__main__':
    import django
    django.setup()
    from registration.models import Profile


import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        created = text_data_json["created"]
        avatar = text_data_json["avatar"]
        full_name = text_data_json["full_name"]

        # format example 12:00 am.

        hour = datetime.datetime.now().strftime("%I:%M %p")

        if "AM" in hour:
            hour = hour.replace("AM", "a.m.")
        else:
            hour = hour.replace("PM", "p.m.")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message,
                                   "username": self.scope["user"].username,
                                   'created': created, 'avatar': avatar, 'hour': hour, 'full_name': full_name})

    # Receive message from room group

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {"message": message,
             "username": event["username"], 'created': event['created'], 'avatar': event['avatar'],
             'hour': event['hour'], 'full_name': event['full_name']}))
        print(event['username'])

import json
from asgiref.sync import sync_to_async
import re
from accounts.models import User

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.auth import get_user

from .models import SenderModel, ReceiverModel, ChatModel, ChatKeyModel
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user1 = await get_user(self.scope)
        user2_pk = self.scope['url_route']['kwargs']['roomName']
        user2 = await self.get_usermodel(pk=user2_pk)
        if not user1.is_authenticated:
            await self.close()
            
        self.user1_username = user1.get_username()
        self.user2_username = user2.get_username()
        self.user1_sender = await self.get_sendermodel(user=user1)
        self.user2_receiver = await self.get_receivermodel(user=user2)
        
        usernames = [self.user1_username]
        if not self.user1_username == self.user2_username:
            # We only add the user2 username to `usernames` list when 
            # it is not the same with user1 username because we don't 
            # want to duplicate it
            usernames.append(self.user2_username)
        chatkey = await database_sync_to_async(ChatKeyModel.get_by_usernames)(usernames)
        self.room_name = f'chat_room_{chatkey.key}'
        # self.room_group_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', f"chat_{user2_pk}")
        # Join room group
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message = {
            'sender': self.user1_sender,
            'receiver': self.user2_receiver,
            'text': message
        }
        # Save the message to database
        await self.create_chatmodel(**message)

        # Get the created ChatModel, format the chat log,
        # then send it to the channel layer
        chatmodel = await self.get_latest_chatmodel(**message)
        log = f'{chatmodel.log.date()} - {str(chatmodel.log.time())[:8]}'
        chatmodel = {
            'sender_username': self.user1_username,
            'receiver_username': self.user2_username,
            'text': chatmodel.text,
            'log': log
        }
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name, {"type": "chat.message", "chatmodel": chatmodel}
        )

    # Receive message from room group
    async def chat_message(self, event):
        # here events are the above dictionary from receive
        message = json.dumps({'chatmodel': event['chatmodel']})

        # Send message to WebSocket
        await self.send(
            text_data=message
        )
        
    @database_sync_to_async
    def get_usermodel(self, **kwargs):
        return User.objects.get(**kwargs)
    
    @database_sync_to_async
    def get_receivermodel(self, **kwargs):
        return ReceiverModel.objects.get(**kwargs)
    
    @database_sync_to_async
    def get_sendermodel(self, **kwargs):
        return SenderModel.objects.get(**kwargs)
    
    @database_sync_to_async
    def get_latest_chatmodel(self, **kwargs):
        return ChatModel.objects.filter(**kwargs).last()
    
    @database_sync_to_async
    def create_chatmodel(self, **kwargs):
        return ChatModel.objects.create(**kwargs)
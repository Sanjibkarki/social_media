import json
from asgiref.sync import sync_to_async
import re
from accounts.models import User
from collections import defaultdict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.auth import get_user
from .models import SenderModel, ReceiverModel, ChatModel, ChatKeyModel, Profile
from django.core.cache import cache

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # This gives sender Email
        self.user1 = await get_user(self.scope)
        # This gives rceiver Email
        self.user2_pk = self.scope['url_route']['kwargs']['roomName']
        user2 = await self.get_usermodel(pk=self.user2_pk)
        self.profileId = await self.get_profile(user = self.user1)
        
        if not self.user1.is_authenticated:
            await self.close()
        
        

        self.user1_username = self.user1.get_username()
        self.user2_username = user2.get_username()
        
        self.user1_sender = await self.get_sendermodel(user=self.user1)
        self.user1_senderchat = await self.get_sendermodelchat(user=self.user1)
        self.user2_receiver = await self.get_receivermodel(user=user2)
        sender = await database_sync_to_async(SenderModel.objects.get)(user=user2)
        receiver = await database_sync_to_async(ReceiverModel.objects.get)(user=self.user1)
        chatseen = await database_sync_to_async(list)(
            ChatModel.objects.filter(sender=sender, receiver=receiver, is_read=False)
        )
        
        usernames = [self.user1_username]
        if not self.user1_username == self.user2_username:
            # We only add the user2 username to `usernames` list when 
            # it is not the same with self.user1 username because we don't 
            # want to duplicate it
            usernames.append(self.user2_username)
        chatkey = await database_sync_to_async(ChatKeyModel.get_by_usernames)(usernames)
        self.room_name = f'chat_room_{chatkey.key}'
        # self.room_group_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', f"chat_{self.user2_pk}")
        # Join room group
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        if chatseen:
            for chat in chatseen:
                chat.is_read = True   
                await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(
                self.room_name, {"type": "info.message", "info": True,"user":self.user2_username }
            )


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json["message"]
        sender_email = self.user1_username

        message = {
            'sender': self.user1_sender,
            'receiver': self.user2_receiver,
            'text': text
        }

        chatmodel = await self.create_chatmodel(**message)
        
        log = f'{chatmodel.log.date()} - {str(chatmodel.log.time())[:8]}'
        chatmodel = {
            'sender_username': self.user1_senderchat,
            'senderId': self.profileId,
            'chatId': chatmodel.id,
            'receiver_username': self.user2_username,
            'text': chatmodel.text,
            'log': log,
        }
        
        await self.channel_layer.group_send(
            self.room_name, {"type": "chat.message", "chatmodel": chatmodel}
        )

    async def info_message(self, event):
        message = json.dumps({'info': event['info'],'user':event['user']})
        await self.send(
            text_data=message
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
    def get_profile(self, **kwargs):
        return Profile.objects.get(**kwargs).id
    
    @database_sync_to_async
    def get_receivermodel(self, **kwargs):
        return ReceiverModel.objects.get(**kwargs)
    
    @database_sync_to_async
    def get_sendermodel(self, **kwargs):
        return SenderModel.objects.get(**kwargs)
    
    @database_sync_to_async
    def get_sendermodelchat(self, **kwargs):
        return SenderModel.objects.get(**kwargs).user.username
    
    @database_sync_to_async
    def get_latest_chatmodel(self, **kwargs):
        return ChatModel.objects.filter(**kwargs).last()
    
    @database_sync_to_async
    def create_chatmodel(self, **kwargs):
        return ChatModel.objects.create(**kwargs)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = await get_user(self.scope)
        
        if not self.user1.is_authenticated:
            await self.close()
            return

        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'user_{self.user_id}' 
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender':sender
            
        }))

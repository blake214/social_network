import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import *

class MessageConsumer(AsyncWebsocketConsumer):
    ''' MessageConsumer
    An async websocket for the thread messages
    '''
    async def connect(self):
        ''' connect
        Creating an async websocket connection
        '''
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_id = 'thread_%s' % self.thread_id

        # Checking joining user is logged in
        session = self.scope.get('session')
        if session:
            self.user_id = session.get('user_id')
        else:
            raise DenyConnection("User session not found. Please log in.")
        # Checking joining user allowed in group
        await database_sync_to_async(self.check_user_thread_junction)(self.thread_id, self.user_id)

        # Join thread group
        await self.channel_layer.group_add(
            self.thread_group_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        ''' disconnect
        Disconnecting from an async websocket connection
        '''
        # Leave thread group
        await self.channel_layer.group_discard(
            self.thread_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        ''' receive
        Recieve message from an async websocket connection
        '''
        # Get session user_id
        session = self.scope.get('session')
        if session:
            user_id = session.get('user_id')
        else:
            raise DenyConnection("User session not found. Please log in.")

        # Get the message that was sent
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to thread group
        await self.channel_layer.group_send(
            self.thread_group_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # Update database
        await database_sync_to_async(self.create_thread_message)(self.thread_id, user_id, message)

    async def chat_message(self, event):
        ''' chat_message
        Receive message from room group
        '''
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # I wrote this code -------------------------- Start
    def create_thread_message(self, thread_id, user_id, message):
        ''' create_thread_message
        Creates a record of the message in the database
        '''
        ThreadMessages.objects.create(
            thread_id=thread_id,
            creating_user_id=user_id,
            message=message
        )

    def check_user_thread_junction(self, thread_id, user_id):
        ''' check_user_thread_junction
        Checks that the user is connected to the thread
        '''
        try:
            user_thread_junction = UserThreadJunctions.objects.get(thread_id=thread_id, user_id=user_id)
        except ObjectDoesNotExist:
            raise DenyConnection("User not allowed in thread.")
        if not user_thread_junction:
            raise DenyConnection("User not allowed in thread.")
    # I wrote this code -------------------------- End

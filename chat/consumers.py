import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib import messages

from chat.models import Message, Chat


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    def new_message(self, data):
        user = get_user_model().objects.get(username=data['username'])
        message = data['message']
        related_chat = Chat.objects.filter(room_name=self.room_name).first()
        if related_chat is None:
            print('User not found')
            # messages.error(request, 'User not found')
        else:
            if user not in related_chat.members.all():
                print('Not allowed')
            else:
                Message.objects.create(owner=user, content=message, related_chat=related_chat)

    def fetch_message(self):
        pass

    command = {
        'new_message': new_message,
        'fetch_message': fetch_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        command = text_data_json['command']
        if command == 'new_message':
            self.new_message(data=text_data_json)
        else:
            self.fetch_message()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'command': 'new_message'
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

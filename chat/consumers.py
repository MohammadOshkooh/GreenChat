import base64

from django.core.files.base import ContentFile
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework.renderers import JSONRenderer

from chat.models import Message, Chat
from .serializers import ChatSerializersWithImage, ChatSerializersWithoutImage


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.related_chat = None
        self.link = None
        self.room_group_name = None
        self.room_name = None

    def new_message(self, data):
        user = get_user_model().objects.get(username=data['username'])

        # save on db
        message_model = Message.objects.create(owner=user, content=data['message'], related_chat=self.related_chat)

        # convert object to json
        message_model_json = self.message_serializers(message_model)

        self.send_to_room({'data': message_model_json, 'command': 'new_message'})

    def fetch_message(self):
        # get message model (with or without image)
        messages_model_with_image = Message.objects.filter(related_chat__room_name=self.room_name,
                                                           related_chat__link=self.link, contain_image=True)
        messages_model_without_image = Message.objects.filter(related_chat__room_name=self.room_name,
                                                              related_chat__link=self.link, contain_image=False)

        count = messages_model_without_image.count() + messages_model_with_image.count()

        messages_model_json = None

        if count != 0:
            # convert object to json
            messages_model_json_without_image = self.message_serializers(messages_model_without_image)
            messages_model_json_with_image = self.message_serializers(messages_model_with_image)
            messages_model_json = messages_model_json_without_image + messages_model_json_with_image

            # sort content_list by created date
            messages_model_json.sort(key=lambda x: x['created'])

        self.send_to_websocket(
            event={'data': messages_model_json, 'command': 'fetch_message', 'count': count})

    def image(self, data):
        user = get_user_model().objects.get(username=data['username'])

        # convert base64 string to image
        file = data['message']
        format, imgstr = file.split(';base64,')
        ext = format.split('/')[-1]
        image_file = ContentFile(base64.b64decode(imgstr), name=get_random_string(6) + '.' + ext)

        # save image on db
        message_model = Message.objects.create(owner=user, image=image_file, related_chat=self.related_chat,
                                               contain_image=True)

        # convert object to json
        message_model_json = self.message_serializers(message_model)

        self.send_to_room({'data': message_model_json, 'command': 'new_message'})

    command = {
        'new_message': new_message,
        'fetch_message': fetch_message,
        'img': image,
    }

    def message_serializers(self, data):
        many = (lambda l: True if data.__class__.__name__ == 'QuerySet' else False)(data)
        obj = (lambda l: data.first() if data.__class__.__name__ == 'QuerySet' else data)(data)

        if obj.contain_image is False:
            serialized = ChatSerializersWithoutImage(data, many=many)
        else:
            serialized = ChatSerializersWithImage(data, many=many)

        content = JSONRenderer().render(data=serialized.data)

        # Fix  NameError: name 'true' is not defined
        false = False
        true = True

        # convert bytes to list
        content_list = eval(content)

        return content_list

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.link = self.scope['url_route']['kwargs']['link']
        self.room_group_name = f'chat_{self.room_name}_{self.link}'
        self.related_chat = Chat.objects.filter(room_name=self.room_name, link=self.link).first()

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

        command = text_data_json['command']

        # check command
        if command == 'new_message':
            self.new_message(data=text_data_json)
        elif command == 'img':
            self.image(data=text_data_json)
        else:
            self.fetch_message()

    # Send message to room group
    def send_to_room(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_to_websocket',
                'data': data['data'],
                'command': data['command'],
                'count': Message.objects.filter(related_chat__room_name=self.room_name,
                                                related_chat__link=self.link).count(),
            }
        )

    # Receive message from room group
    def send_to_websocket(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'event': event
        }))

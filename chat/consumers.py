import base64

from django.core.files.base import ContentFile
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework.renderers import JSONRenderer

from accounts.api.serializers import UserSerializers
from chat.models import Message, Chat
from chat.api.serializers import ChatSerializers, MessageSerializers


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None
        self.user = None

    def new_message(self, data, contain_image=False):
        """
        Receive new message from websocket and save on the db
        :param data:
        :param contain_image:
        :return:
        """
        user = self.user
        message = data['message']
        chat_room = Chat.objects.get(id=message['recvId'])

        if contain_image is True:
            # convert base64 string to image
            file = message['image']
            format, imgstr = file.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name=get_random_string(6) + '.' + ext)

            # save image on db
            message_model = Message.objects.create(sender=user, image=image_file, related_chat=chat_room,
                                                   time=message['time'], status=message['status'],
                                                   received_from_the_group=message['recvIsGroup'], contain_image=True)

            # convert object to json
            message_model_json = self.serializers(message_model, MessageSerializers)

            self.send_to_room({'data': message_model_json, 'command': 'new_message', 'contain_image': True})

        else:
            # save on db
            message_model = Message.objects.create(sender=user, body=message['body'], related_chat=chat_room,
                                                   time=message['time'], status=message['status'],
                                                   received_from_the_group=message['recvIsGroup'])

            # convert object to json
            message_model_json = self.serializers(message_model, MessageSerializers)

            self.send_to_room({'data': message_model_json, 'command': 'new_message', 'contain_image': False})

    def fetch(self):

        self.send_to_websocket(
            event={'command': 'fetch'})

    def serializers(self, data, serializers_class):
        """
        Serializing the data passed to it
        :param data:
        :param serializers_class:
        :return: Serializing and then to jsan and finally convert to eval and return theme
        """
        many_value = (lambda l: True if data.__class__.__name__ == 'QuerySet' else False)(data)

        if serializers_class in [ChatSerializers, UserSerializers]:
            many_value = True

        serialized = serializers_class(data, many=many_value)

        content = JSONRenderer().render(data=serialized.data)

        # Fix  NameError: name 'true' is not defined
        false = False
        true = True

        # convert bytes to list
        content_list = eval(content)

        return content_list

    command = {
        'new_message': new_message,
        'fetch': fetch,
    }

    def connect(self):
        self.room_group_name = 'chat'

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

        # assign user
        self.user = get_user_model().objects.get(username=text_data_json['username'])

        command = text_data_json['command']

        # check command
        if command == 'new_message':
            self.new_message(data=text_data_json, contain_image=text_data_json['contain_image'])
        elif command == 'fetch':
            self.fetch()

    # Send message to room group
    def send_to_room(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_to_websocket',
                'data': data['data'],
                'command': data['command'],
            }
        )

    # Receive message from room group
    def send_to_websocket(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'event': event
        }))

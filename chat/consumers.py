import base64

from django.core.files.base import ContentFile
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework.renderers import JSONRenderer

from accounts.api.serializers import UserSerializers
from chat.models import Message, Chat, ContactList
from chat.api.serializers import ChatSerializers, MessageSerializers, ContactListSerializers


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.related_chat = None
        self.link = None
        self.room_group_name = None
        self.room_name = None
        self.user = None

    def new_message(self, data, contain_image):
        """
        Receive new message from websocket and save on the db
        :param data:
        :param contain_image:
        :return:
        """
        user = self.user

        if contain_image is True:
            # convert base64 string to image
            file = data['message']
            format, imgstr = file.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name=get_random_string(6) + '.' + ext)

            # save image on db
            message_model = Message.objects.create(sender=user, image=image_file, related_chat=self.related_chat,
                                                   contain_image=True)

            # convert object to json
            message_model_json = self.serializers(message_model, MessageSerializers)

            self.send_to_room({'data': message_model_json, 'command': 'new_message', 'contain_image': True})

        else:
            # save on db
            message_model = Message.objects.create(sender=user, body=data['message'], related_chat=self.related_chat)

            # convert object to json
            message_model_json = self.serializers(message_model, MessageSerializers)

            self.send_to_room({'data': message_model_json, 'command': 'new_message', 'contain_image': False})

    def fetch(self):
        """
        Fetch data from db
        :return:  send fetched data to websocket
        """
        messages = self.get_messages()
        group_list = self.get_group_list()
        contact_list = self.get_contact_list()

        self.send_to_websocket(
            event={'messages': messages, 'group_list': group_list, 'contact_list': contact_list,
                   'user_info': self.get_user_info(), 'all_users': self.get_all_users_list(), 'command': 'fetch'})

    def get_messages(self):
        """
        fetch messages from db and serialized and then convert to json
        :return: messages json
        """
        # get message model (with or without image)
        messages_model_with_image = Message.objects.filter(related_chat__room_name=self.room_name,
                                                           related_chat__link=self.link, contain_image=True)
        messages_model_without_image = Message.objects.filter(related_chat__room_name=self.room_name,
                                                              related_chat__link=self.link, contain_image=False)

        count = messages_model_without_image.count() + messages_model_with_image.count()

        messages_model_json = []

        if messages_model_without_image.count() != 0:
            # convert object to json
            messages_model_json_without_image = self.serializers(messages_model_without_image, MessageSerializers)
            messages_model_json += messages_model_json_without_image
        if messages_model_with_image.count() != 0:
            messages_model_json_with_image = self.serializers(messages_model_with_image, MessageSerializers)
            messages_model_json += messages_model_json_with_image
        if count != 0:
            # sort content_list by created date
            messages_model_json.sort(key=lambda x: x['time'])
        return messages_model_json

    def get_group_list(self):
        """
        fetch group list from db and serialized and then convert to json
        :return: group list json
        """
        group_list = []

        for chat in Chat.objects.all():
            if self.user in chat.members.all():
                group_list.append(chat)

        group_list_json = self.serializers(data=group_list, serializers_class=ChatSerializers)
        return group_list_json

    def get_contact_list(self):
        """
        fetch contact list from db and serialized and then convert to json
        :return: contact list json
        """
        all_users = get_user_model().objects.all()

        contact_list_model = ContactList.objects.filter(owner=self.user).first()

        contact_list = []

        for user in all_users:
            if user in contact_list_model.contact.all():
                contact_list.append(user)

        contact_list_json = self.serializers(data=contact_list, serializers_class=UserSerializers)

        return contact_list_json

    def get_user_info(self):
        """
        get user current info
        :return: user info json
        """
        user_model = [get_user_model().objects.get(username=self.user.username)]
        user_model_json = self.serializers(data=user_model, serializers_class=UserSerializers)
        return user_model_json

    def get_all_users_list(self):
        """
        get all users  list
        :return: all users list json
        """
        users_list = get_user_model().objects.all()
        users_list_json = self.serializers(users_list, UserSerializers)
        return users_list_json

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

        # assign user
        self.user = get_user_model().objects.get(username=text_data_json['username'])

        command = text_data_json['command']

        # check command
        if command == 'new_message':
            self.new_message(data=text_data_json)
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

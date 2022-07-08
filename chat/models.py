from django.contrib.auth import get_user_model
from django.db import models


class Chat(models.Model):
    room_name = models.CharField(max_length=50)
    members = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.room_name


class Message(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.username

    def get_message(self, room_name):
        return Message.objects.filter(related_chat__room_name=room_name).order_by('-created')

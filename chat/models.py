from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

from accounts.models import CustomUser


class Chat(models.Model):
    room_name = models.CharField(max_length=50)
    members = models.ManyToManyField(get_user_model(), related_name='member_set')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='owner_set', null=True)
    image = models.ImageField(upload_to='profile/group/%y/%m/%d/', blank=True, null=True,
                              default='../static/img/index.png')
    link = models.CharField(default=get_random_string(20), max_length=50, unique=True)

    def __str__(self):
        return self.room_name

    def get_absolute_url(self):
        return reverse('chat:chat', args=[self.room_name, self.link])

    def is_join(self, user):
        if user in self.members.all():
            return True
        return False


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True, default='body')
    time = models.DateTimeField(auto_now_add=True)
    # message status = 0:sent, 1:delivered, 2:read
    status = models.IntegerField(default=0)
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chat/image/%y/%m/%d/', blank=True, null=True,
                              default='../static/img/index.png')
    contain_image = models.BooleanField(default=False)
    Received_from_the_group = models.BooleanField()

    def __str__(self):
        return self.sender.username

    def get_message(self, room_name):
        return Message.objects.filter(related_chat__room_name=room_name).order_by('-created')


class ContactList(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact = models.ManyToManyField(get_user_model(), related_name='contact_list')

    def __str__(self):
        return self.owner.username

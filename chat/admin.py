from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Chat, Message, ContactList
from django.contrib.auth.admin import UserAdmin


class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'body', 'time', 'related_chat', 'status']


admin.site.register(Message, MessageAdmin)

admin.site.register(Chat)

admin.site.register(ContactList)

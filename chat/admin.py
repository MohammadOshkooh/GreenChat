from django.contrib import admin

from .models import Chat, Message, ContactList


class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'body', 'time', 'related_chat', 'status']


admin.site.register(Message, MessageAdmin)

admin.site.register(Chat)

admin.site.register(ContactList)

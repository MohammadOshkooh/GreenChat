from django.contrib import admin

from .models import Chat, Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'created', 'owner', 'related_chat']


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)

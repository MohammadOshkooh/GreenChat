from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.models import Message, Chat


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super(ChatView, self).get_context_data(**kwargs)
        room_name = self.kwargs.get('room_name')
        context['room_name'] = room_name
        user = self.request.user
        context['username'] = user.username
        context['messages'] = Message.objects.filter(related_chat__room_name=room_name)
        chat = Chat.objects.filter(room_name=room_name).first()
        context['chat'] = chat

        return context

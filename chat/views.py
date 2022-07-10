from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.models import Message


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'


class Chat(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super(Chat, self).get_context_data(**kwargs)
        room_name = self.kwargs.get('room_name')
        context['room_name'] = room_name
        user = self.request.user
        context['username'] = user.username
        context['messages'] = Message.objects.filter(related_chat__room_name=room_name)
        return context

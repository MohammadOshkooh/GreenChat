from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'chat/index.html'


class Chat(TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super(Chat, self).get_context_data(**kwargs)
        room_name = self.kwargs.get('room_name')
        context['room_name'] = room_name
        context['username'] = self.request.user.username
        return context

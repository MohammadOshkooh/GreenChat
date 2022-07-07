from django.shortcuts import render
from django.views.generic import TemplateView


class Chat(TemplateView):
    template_name = 'chat/room.html'


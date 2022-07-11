from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Profile
from chat.models import Message, Chat
from .forms import CreateNewGroupForm


class Index(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'chat/index.html'
    form_class = CreateNewGroupForm

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        if profile is None:
            profile = Profile.objects.create(user=user)
        context['profile'] = profile

        chats = []
        for chat in Chat.objects.all():
            if chat.is_join(user):
                chats.append(chat)
        context['chats'] = chats

        return context

    def form_valid(self, form):
        room_name = form.cleaned_data.get('room_name').replace(' ', '_')
        form = form.save(commit=False)
        form.room_name = room_name
        user = self.request.user
        form.owner = user
        form.save()
        form.members.add(user)
        return redirect(Chat.objects.get(room_name=room_name).get_absolute_url())


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

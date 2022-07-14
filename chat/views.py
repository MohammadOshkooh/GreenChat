import os

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import ProfileForm
from accounts.models import Profile
from chat.models import Message, Chat
from .forms import CreateNewGroupForm


@login_required
def index(request):
    user = request.user

    # user profile
    profile = Profile.objects.filter(user=user).first()
    if profile is None:
        profile = Profile.objects.create(user=user)

    # user chats
    chats = []
    for chat in Chat.objects.all():
        if chat.is_join(user):
            chats.append(chat)

    if request.method == 'POST':
        # create new group
        create_new_group_form = CreateNewGroupForm(request.POST)
        if create_new_group_form.is_valid():
            room_name = create_new_group_form.cleaned_data.get('room_name').replace(' ', '_')
            new_chat = Chat.objects.create(room_name=room_name, owner=request.user)
            new_chat.members.add(request.user)
            # create_new_group_form = create_new_group_form.save(commit=False)
            # create_new_group_form.room_name = room_name
            # create_new_group_form.owner = user
            # create_new_group_form.save()
            # create_new_group_form.members.add(user)
            return redirect(Chat.objects.filter(room_name=room_name).last().get_absolute_url())

        # update profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            # deleting old uploaded image
            img_path = profile.image.path
            if os.path.exists(img_path):
                os.remove(img_path)
            profile_form.save()

    else:
        create_new_group_form = CreateNewGroupForm()
        profile_form = ProfileForm()

    context = {
        'profile': profile,
        'chats': chats,
        'create_new_group_form': create_new_group_form,
        'profile_form': profile_form,
    }

    return render(request, 'chat/index.html', context)


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super(ChatView, self).get_context_data(**kwargs)
        room_name = self.kwargs.get('room_name')
        context['room_name'] = room_name
        context['link'] = self.kwargs.get('link')
        context['messages'] = Message.objects.filter(related_chat__room_name=room_name)
        context['chat'] = Chat.objects.filter(room_name=room_name).first()
        return context

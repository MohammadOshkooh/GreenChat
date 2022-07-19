import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from accounts.forms import ProfileForm
from accounts.models import Profile
from chat.models import Message, Chat
from .forms import CreateNewGroupForm, UpdateChatProfileForm


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

    # search for group in search bar by chat room link
    group_link = request.GET.get('link')
    if group_link is not None:
        chat = Chat.objects.filter(link=group_link).first()

        # ّّif chat is exist
        if chat is not None:
            # If the user was not a member of the group
            if user not in chat.members.all():
                # user join
                chat.members.add(user)
            # go to chat room
            return redirect(chat.get_absolute_url())
        else:
            # chat not found
            return render(request, 'chat/404.html', {})

    if request.method == 'POST':
        # create new group
        create_new_group_form = CreateNewGroupForm(request.POST)
        if create_new_group_form.is_valid():
            room_name = create_new_group_form.cleaned_data.get('room_name').replace(' ', '_')

            # create
            new_chat = Chat.objects.create(room_name=room_name, owner=request.user, link=get_random_string(22))

            # user join
            new_chat.members.add(request.user)
            return redirect(new_chat.get_absolute_url())

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


@login_required
def chat_view(request, room_name, link):
    messages = Message.objects.filter(related_chat__room_name=room_name, related_chat__link=link)
    chat = Chat.objects.filter(room_name=room_name, link=link).first()

    # if chat not exist
    if chat is None:
        return render(request, 'chat/404.html', {})

    if request.method == 'POST':
        # update chat-profile
        chat_profile_form = UpdateChatProfileForm(request.POST, request.FILES, instance=chat)
        if chat_profile_form.is_valid():
            # deleting old update image
            img_path = chat.image.url
            if os.path.exists(img_path):
                os.remove(img_path)
            # save new image
            chat_profile_form.save()
    else:
        chat_profile_form = UpdateChatProfileForm()

    context = {
        'messages': messages,
        'chat': chat,
        'chat_profile_form': chat_profile_form,
        'room_name': room_name,
        'link': link,
    }
    return render(request, 'chat/room.html', context)

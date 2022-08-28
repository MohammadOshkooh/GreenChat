from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string

from accounts.forms import ProfileForm
from chat.models import Message, Chat, ContactList
from .forms import UpdateGroupName, UpdateGroupLink


@login_required
def chat(request):
    contact_list = ContactList.objects.filter(owner=request.user).first()
    if contact_list is None:
        contact_list = ContactList.objects.create(owner=request.user)

    # user instance
    user_model = get_user_model().objects.get(username=request.user)

    if request.method == 'POST':
        print(request.POST)
        # Update profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_model)
        if profile_form.is_valid():
            if request.FILES:
                # update profile photo
                profile_form = profile_form.save(commit=False)
                profile_form.image = request.FILES['image']
            profile_form.save()

        # Create new group
        group_name = request.POST.get('new-group-name')

        if group_name is not None:
            new_chat = Chat.objects.create(room_name=group_name, owner=request.user,
                                           link=get_random_string(21))

            # user join
            new_chat.members.add(request.user)

            # create first message
            Message.objects.create(sender=request.user, body='Hello... I am the owner of this group', status=1,
                                   related_chat=new_chat, received_from_the_group=True)

        # Join (after search in search bar)
        join_input = request.POST.get('join-input')
        if join_input is not None:
            search_chat = Chat.objects.get(id=join_input)
            search_chat.members.add(request.user)

        # Update group name
        chat_id = request.POST.get('update-group-name-id')
        if chat_id is not None:
            update_group_name_form = UpdateGroupName(request.POST, instance=Chat.objects.get(id=chat_id))
            chat_id = None
            if update_group_name_form.is_valid():
                update_group_name_form.save()

        # Update group link
        chat_id = request.POST.get('update-group-link-id')
        if chat_id is not None:
            update_group_link_form = UpdateGroupLink(request.POST, instance=Chat.objects.get(id=chat_id))
            if update_group_link_form.is_valid():
                update_group_link_form.save()

        # Leave group
        group_id = request.POST.get('group-id')
        if group_id is not None:
            chat = Chat.objects.get(id=group_id)
            chat.members.remove(request.user)

        return redirect(reverse('chat:chat'))
    else:
        profile_form = ProfileForm(instance=user_model)
        update_group_name_form = UpdateGroupName()
        update_group_link_form = UpdateGroupLink()

    context = {
        'update_group_name_form': update_group_name_form,
        'update_group_link_form': update_group_link_form,
        'profile_form': profile_form,
        'contact_list': contact_list,
        'user': request.user  # used in js
    }
    return render(request, 'chat/index.html', context)

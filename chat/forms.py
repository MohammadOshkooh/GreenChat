from django import forms

from chat.models import Chat


class CreateNewGroupForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['room_name']

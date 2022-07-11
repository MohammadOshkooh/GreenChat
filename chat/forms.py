from django import forms

from chat.models import Chat


class CreateNewGroupForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['room_name']
        widgets = {
            'room_name': forms.Textarea(
                attrs={'id': "chat-message-input", 'name': "", 'class': "form-control type_msg",
                       'placeholder': "create new group (Enter group name)",
                       'style': "height: 12px;margin-left: 21px;width: 86%;"})
        }

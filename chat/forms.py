from django import forms

from chat.models import Chat


class UpdateChatProfileForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['image']


class CreateNewGroupForm(forms.Form):
    room_name = forms.CharField(widget=forms.Textarea(
        attrs={'id': "chat-message-input", 'name': "", 'class': "form-control type_msg",
               'placeholder': "create new group (Enter group name)",
               'style': "height: 12px;margin-left: 21px;width: 86%;"
               }))


class UpdateGroupName(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['room_name', 'id']
        widgets = {
            'room_name': forms.TextInput(attrs={'style': 'display:none', 'id': 'update-group-name'})
        }


class UpdateGroupLink(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['link', 'id']
        widgets = {
            'link': forms.TextInput(attrs={'style': 'display:none', 'id': 'update-group-link'})
        }

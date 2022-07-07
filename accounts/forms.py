from allauth.account.forms import LoginForm
from django import forms


class CustomLoginForm(LoginForm):
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', }), max_length=100)
    # login_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}), max_length=250)
    #

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'input100'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'input100'})

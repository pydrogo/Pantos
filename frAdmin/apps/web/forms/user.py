from django.forms import ModelForm
from frAdmin.apps.web.models import UserProfile
from django.contrib.auth.models import User
from frAdmin.apps.web.managers.user_manager import UserManager
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active']
        Widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailField(),

        }

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

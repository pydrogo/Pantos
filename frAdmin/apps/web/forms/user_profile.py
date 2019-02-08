from django.forms import ModelForm
from frAdmin.apps.web.models import UserProfile
from django.contrib.auth.models import User
from frAdmin.apps.web.managers.user_manager import UserManager
from django.contrib.auth.models import Group as GroupDjango
from django import forms


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['pass_limitation', 'mobile', 'unit', 'group', 'image_profile', 'last_pass', 'black_list']

        Widgets = {
            'mobile': forms.IntegerField(),
        }
        error_messages = {
            'image_profile': {
                'invalid': ("Image files only")
            }
        }

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = GroupDjango.objects.all()

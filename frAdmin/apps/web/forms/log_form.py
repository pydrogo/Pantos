from django.forms import ModelForm
from frAdmin.apps.web.models import Log
from django.contrib.auth.models import User
from frAdmin.apps.web.managers.log_manager import LogManager
from django import forms


class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = ['username', 'date', 'description','action']

    objects = LogManager()

    def __init__(self, *args, **kwargs):
        super(LogForm, self).__init__(*args, **kwargs)
        self.fields['username'].queryset = User.objects.all()

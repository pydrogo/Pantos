from django.forms import ModelForm
from frAdmin.apps.web.models import Camera
from django import forms

class CameraForm(ModelForm):
    class Meta:
        model = Camera
        fields = ['name', 'ip', 'username', 'password']


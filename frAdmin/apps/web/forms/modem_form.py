from django.forms import ModelForm
from frAdmin.apps.web.models.modem import Modem
from frAdmin.apps.web.models.raspberry import Raspberry
from frAdmin.apps.web.managers.modem import ModemManager
from django import forms


class ModemForm(ModelForm):
    class Meta:
        model = Modem
        fields = ['raspberry', 'ssid', 'password']

    objects = ModemManager()

    def __init__(self, *args, **kwargs):
        super(ModemForm, self).__init__(*args, **kwargs)
        self.fields['raspberry'].queryset = Raspberry.objects.all()

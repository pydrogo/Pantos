from django.forms import ModelForm

from frAdmin.apps.web.models import AuthorizedTime


class AuthorizedTimeForm(ModelForm):
    class Meta:
        model = AuthorizedTime
        fields = ['authorized_day','start_hour','end_hour']



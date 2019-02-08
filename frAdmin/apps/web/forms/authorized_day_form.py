from django.forms import ModelForm

from frAdmin.apps.web.models import AuthorizedDay


class AuthorizedDayForm(ModelForm):
    class Meta:
        model = AuthorizedDay
        fields = ['date','group','start','end']


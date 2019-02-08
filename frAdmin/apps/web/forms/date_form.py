from django.forms import ModelForm
from frAdmin.apps.web.models import Date


class DateForm(ModelForm):
    class Meta:
        model = Date

        fields = ['day','day_number']
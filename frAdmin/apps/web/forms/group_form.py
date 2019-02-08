from django.forms import ModelForm
from frAdmin.apps.web.models import Group
from frAdmin.apps.web.managers import GroupManager


class GroupFrom(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'welcome_voice', 'active_rele_time']

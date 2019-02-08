from django.forms import ModelForm, PasswordInput
from frAdmin.apps.web.models import Raspberry


class RaspberryForm(ModelForm):
    class Meta:
        model = Raspberry

        fields = ['name', 'ip', 'sub_netmask', 'dhcp', 'default_gateway', 'video_intro','play_video_intro', 'unkown_person',
                  'ftp_path','ftp_username','ftp_password']

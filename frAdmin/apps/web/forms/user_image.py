from django.forms import ModelForm
from frAdmin.apps.web.models import UserImage, UserProfile
from frAdmin.apps.web.managers.image_manager import UserImageManager


class UserImageForm(ModelForm):
    class Meta:
        model = UserImage
        fields = ['user', 'profile_image']

    objects = UserImageManager()

    def __init__(self, *args, **kwargs):
        super(UserImageForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all()

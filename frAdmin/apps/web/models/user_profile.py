from django.db import models
import os
from django.dispatch import receiver
from django.contrib.auth.models import User
from frAdmin.apps.web.managers.user_manager import UserManager
from . import Base
from django.contrib.auth.models import Group as GroupDjango
from frAdmin.apps.web.utils.user_image_path import get_user_file_path
from django.core.validators import FileExtensionValidator


class UserProfile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    mobile = models.IntegerField(null=False)
    unit = models.CharField(null=False, max_length=50)
    group = models.ForeignKey(GroupDjango, on_delete=models.CASCADE, blank=True)
    image_profile = models.FileField(upload_to=get_user_file_path,
                                     validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    pass_limitation = models.IntegerField(null=False, default=00000)
    last_pass = models.DateTimeField(null=True, blank=True)
    counter = models.IntegerField(null=False, default=0)
    last_snapshot = models.CharField(null=True, max_length=100, blank=True)

    black_list = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.user.first_name


@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image_profile:
        if os.path.isfile(instance.image_profile.path):
            os.remove(instance.image_profile.path)

def save(self, *args, **kwargs):
    return super(UserProfile, self).save(*args, **kwargs)



@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = UserProfile.objects.get(pk=instance.pk).image_profile
    except UserProfile.DoesNotExist:
        return False

    new_file = instance.image_profile
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

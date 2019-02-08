import os
from django.db import models
from django.dispatch import receiver
from . import Base
from frAdmin.apps.web.managers.image_manager import UserImageManager
from frAdmin.apps.web.utils.content_type_restricted_file_field import ContentTypeRestrictedFileField
from .user_profile import UserProfile
from frAdmin.apps.web.utils.user_image_path import get_file_path
from django.core.validators import FileExtensionValidator


class UserImage(Base):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to=get_file_path, max_length=500,
                                     validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], blank=True)

    objects = UserImageManager()

    class Meta:
        db_table = 'userimage'

    def __str__(self):
        return self.user.user.username


@receiver(models.signals.post_delete, sender=UserImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)


@receiver(models.signals.pre_save, sender=UserImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = UserImage.objects.get(pk=instance.pk).profile_image
    except UserImage.DoesNotExist:
        return False

    new_file = instance.profile_image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


def save(self, *args, **kwargs):
    # object is possibly being updated, if so, clean up.
    return super(UserImage, self).save(*args, **kwargs)

from django.db import models
from frAdmin.apps.web.managers.group_manager import GroupManager
from . import Base
from frAdmin.apps.web.models.alarms import Alarms
from django.contrib.auth.models import Group as GroupDjango
from django.dispatch import receiver
import os


class Group(Base):
    group = models.OneToOneField(GroupDjango, on_delete=models.CASCADE)
    alarm = models.ManyToManyField(Alarms)

    name = models.CharField(null=False, max_length=50)
    welcome_voice = models.FileField(upload_to='welcome_voice', null=False, blank=True)
    active_rele_time = models.IntegerField(null=False)

    # email_to_boss = models.BooleanField(null=False, default=False)
    # email_to_person = models.BooleanField(null=False, default=False)
    # take_picture = models.BooleanField(null=False, default=True)
    # rele_number = models.IntegerField(null=False)

    objects = GroupManager()

    class Meta:
        db_table = 'group'

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Group)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.welcome_voice:
        if os.path.isfile(instance.welcome_voice.path):
            os.remove(instance.welcome_voice.path)


@receiver(models.signals.pre_save, sender=Group)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Group.objects.get(pk=instance.pk).welcome_voice
    except Group.DoesNotExist:
        return False

    new_file = instance.welcome_voice
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

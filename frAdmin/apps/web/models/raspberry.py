import requests
from django.db import models
from .base import Base
from frAdmin.apps.web.managers import RaspberryManager
import os
from django.dispatch import receiver
from django.db.models import signals
import json


class Raspberry(Base):
    name = models.CharField(null=False, max_length=50, unique=True)
    ip = models.CharField(null=True, max_length=15, blank=True)
    sub_netmask = models.CharField(null=True, max_length=15, blank=True)
    default_gateway = models.CharField(null=True, max_length=15, blank=True)
    dhcp = models.BooleanField(null=False, default=False)
    unkown_person = models.BooleanField(null=False, default=False)
    play_video_intro = models.BooleanField(null=False, default=False)
    video_intro = models.FileField(upload_to='video_introduct/', null=True, verbose_name="ویدئو", blank=True)
    ftp_path = models.CharField(null=True, max_length=200, blank=True)
    ftp_username = models.CharField(null=True, max_length=200, blank=True)
    ftp_password = models.CharField(null=True, max_length=200, blank=True)
    lock_status = models.BooleanField(null=False, default=False)

    objects = RaspberryManager()

    class Meta:
        db_table = 'raspberry'

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Raspberry)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.video_intro:
        if os.path.isfile(instance.video_intro.path):
            os.remove(instance.video_intro.path)


@receiver(models.signals.pre_save, sender=Raspberry)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Raspberry.objects.get(pk=instance.pk).video_intro
    except Raspberry.DoesNotExist:
        return False

    new_file = instance.video_intro
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except Exception as e:
            print(e)


def change_raspberry(sender, instance, created, **kwargs):
    try:
        if instance.lock_status:
            res = requests.get('http://localhost:8888/StatusEncrypt', data=json.dumps({'encrypt': True}))
        else:
            res = requests.get('http://localhost:8888/StatusEncrypt', data=json.dumps({'encrypt': False}))
    except Exception as e:
        print(str(e))


signals.post_save.connect(receiver=change_raspberry, sender=Raspberry)

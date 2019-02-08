from django.db import models
from .base import Base
from frAdmin.apps.web.managers import RaspberryManager


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

    objects = RaspberryManager()

    class Meta:
        db_table = 'raspberry'

    def __str__(self):
        return self.name

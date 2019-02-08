from django.db import models
from .base import Base
from frAdmin.apps.web.managers import CameraManager


class Camera(Base):
    name = models.CharField(null=False, max_length=50)
    ip = models.CharField(null=False, max_length=15)
    username = models.CharField(null=False, max_length=20)
    password = models.CharField(null=False, max_length=20)

    is_active = models.BooleanField(default=False)

    objects = CameraManager()

    class Meta:
        db_table = 'camera'

    def __str__(self):
        return self.name

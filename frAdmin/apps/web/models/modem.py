from django.db import models
from .base import Base
from frAdmin.apps.web.managers import ModemManager
from frAdmin.apps.web.models.raspberry import Raspberry


class Modem(Base):
    raspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE)
    ssid = models.CharField(null=False, max_length=30)
    password = models.CharField(null=False, max_length=50)
    objects = ModemManager()

    class Meta:
        db_table = 'modem'

    def __str__(self):
        return self.ssid

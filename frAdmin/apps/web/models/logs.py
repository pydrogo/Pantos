from django.db import models
from .base import Base
from django.contrib.auth.models import User
from frAdmin.apps.web.managers.log_manager import LogManager


class Log(Base):
    date = models.DateTimeField(null=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField(blank=True, null=True, max_length=50)
    description = models.TextField(blank=True)
    result = models.BooleanField(blank=True)
    objects = LogManager()
    class Meta:
        db_table = 'logs'

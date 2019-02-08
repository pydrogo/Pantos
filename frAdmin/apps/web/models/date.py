from django.db import models
from .base import Base
from frAdmin.apps.web.managers.date_manager import DateManager


class Date(Base):
    day = models.CharField(default=None, max_length=50)
    day_number = models.IntegerField(null=False, )

    objects = DateManager()

    class Meta:
        db_table = 'date'

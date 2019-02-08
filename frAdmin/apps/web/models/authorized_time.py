from django.db import models
from .base import Base
from .authorized_day import AuthorizedDay
from frAdmin.apps.web.managers import AuthorizedtimeManager

class AuthorizedTime(Base):
    start_hour = models.CharField(null=False ,max_length=8)
    end_hour = models.CharField(null=False,max_length=8)
    authorized_day = models.ForeignKey(AuthorizedDay, on_delete=models.CASCADE)

    objects = AuthorizedtimeManager()

    class Meta:
        db_table = 'authorized_time'

    def __str__(self):
        return str(self.start_hour)+'-' +str(self.end_hour)
from django.db import models
from .base import Base
from .custom_group import Group
from .date import Date
from frAdmin.apps.web.managers import AuthorizedDayManager

class AuthorizedDay(Base):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    start = models.CharField(null=False,max_length=8)
    end = models.CharField(null=False,max_length=8)

    objects = AuthorizedDayManager()

    class Meta:
        db_table = 'authorized_day'

    def __str__(self):
        return str(self.group.name) + str(self.date)


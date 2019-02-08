from django.db import models
from . import Base

class Alarms(Base):
    name = models.CharField(default=None,max_length=30)
    title = models.CharField(default=None,max_length=30)
    description = models.CharField(default=None,max_length=100)
    status = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = 'alarms'


# welcome_voice = models.FileField(upload_to='welcome_voice', null=False)
# email_to_boss = models.BooleanField(null=False, default=False)
# email_to_person = models.BooleanField(null=False, default=False)
# take_picture = models.BooleanField(null=False, default=True)
# show_profile_image = models.BooleanField(null=False, default=True)
# rele_1 = models.BooleanField(null=False, default=True)
# rele_2 = models.BooleanField(null=False, default=True)
# rele_3 = models.BooleanField(null=False, default=True)
from django.db import models
from django.contrib.auth.models import User
from frAdmin.apps.web.managers.user_manager import UserManager
from . import Base
from django.contrib.auth.models import Group as GroupDjango
from frAdmin.apps.web.utils.user_image_path import get_user_file_path
from django.core.validators import FileExtensionValidator


class UserProfile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    mobile = models.IntegerField(null=False, max_length=12)
    unit = models.CharField(null=False, max_length=50)
    group = models.ForeignKey(GroupDjango, on_delete=models.DO_NOTHING, blank=True)
    image_profile = models.FileField(upload_to=get_user_file_path,
                                     validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    pass_limitation = models.IntegerField(null=False, default=00000)
    last_pass = models.DateTimeField(null=True, blank=True)
    counter = models.IntegerField(null=False, max_length=50, default=0)
    last_snapshot = models.CharField(null=True, max_length=100, blank=True)

    black_list = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.user.first_name

    # def remove_on_image_update(self):
    #     try:
    #         # is the object in the database yet?
    #         obj = UserProfile.objects.get(id=self.id)
    #     except UserProfile.DoesNotExist:
    #         # object is not in db, nothing to worry about
    #         return
    #     # is the save due to an update of the actual image file?
    #     for item in obj.image_profile:
    #
    #         if item and self.image_profile and item != self.image_profile:
    #             # delete the old image file from the storage in favor of the new file
    #             item.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.image_profile.delete()
        return super(UserProfile, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        # self.remove_on_image_update()
        return super(UserProfile, self).save(*args, **kwargs)

from django.contrib import admin
from frAdmin.apps.web.models import Group, Date, AuthorizedDay, AuthorizedTime, UserProfile, UserImage, Alarms, Log, \
    Raspberry, Modem,Camera

admin.site.register(Group)
admin.site.register(Date)
admin.site.register(AuthorizedTime)
admin.site.register(AuthorizedDay)
admin.site.register(Alarms)
admin.site.register(Raspberry)
admin.site.register(Modem)
admin.site.register(Camera)


class LogAdmin(admin.ModelAdmin):
    list_display = ("username", "action", "result", "date")
    ordering = ['date']
    readonly_fields = ("date",)
    search_fields = ("username",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "unit", "mobile")
    ordering = ['user']
    readonly_fields = ("user", "image_profile")
    search_fields = ("group", "user")


class UserImageAdmin(admin.ModelAdmin):
    ordering = ['user']
    readonly_fields = ("profile_image",)
    search_fields = ("user",)


admin.site.register(Log, LogAdmin)
admin.site.register(UserImage, UserImageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

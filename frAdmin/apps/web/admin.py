from django.contrib import admin
from frAdmin.apps.web.models import Group, Date, AuthorizedDay, AuthorizedTime, UserProfile, UserImage, Alarms, Log, \
    Raspberry, Modem, Camera


class LogAdmin(admin.ModelAdmin):
    list_display = ("username", "action", "result", "date")
    ordering = ['date']
    # readonly_fieldslds = ("date", "username", "action", "result", "description")
    search_fields = ("username", "action", "result")


class CameraAdmin(admin.ModelAdmin):
    list_display = ("ip", "username", "password", "name")
    ordering = ['name']
    search_fields = ("name", "ip", "username")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "unit", "mobile")
    ordering = ['user']
    readonly_fields = ("user", "image_profile")
    search_fields = ("group", "user")


class UserImageAdmin(admin.ModelAdmin):
    ordering = ['user']
    readonly_fields = ("profile_image",)
    search_fields = ("user",)


class RaspberryAdmin(admin.ModelAdmin):
    list_display = ("name", "ip", "sub_netmask", "default_gateway", "unkown_person", "dhcp")
    ordering = ['name']
    search_fields = ("name", "ip")


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "active_rele_time",)
    ordering = ['name']
    search_fields = ("name", "group")


class AlarmsAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "description", "status",)
    ordering = ['name']
    search_fields = ("name", "title")


class DateAdmin(admin.ModelAdmin):
    list_display = ("day", "day_number")
    ordering = ['day_number']
    readonly_fields = ("day", "day_number")
    search_fields = ("day", "day_number")


class AuthorizedDayAdmin(admin.ModelAdmin):
    list_display = ("group", "date")
    ordering = ['group']
    search_fields = ("date",)


class AuthorizedTimeAdmin(admin.ModelAdmin):
    list_display = ("authorized_day",)
    ordering = ['authorized_day']


class ModemAdmin(admin.ModelAdmin):
    list_display = ("raspberry", "ssid", "password")
    ordering = ['raspberry']
    search_fields = ("raspberry", "ssid")


admin.site.register(Log, LogAdmin)
admin.site.register(UserImage, UserImageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Raspberry, RaspberryAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Alarms, AlarmsAdmin)
admin.site.register(Date, DateAdmin)
admin.site.register(AuthorizedTime, AuthorizedTimeAdmin)
admin.site.register(AuthorizedDay, AuthorizedDayAdmin)
admin.site.register(Modem, ModemAdmin)

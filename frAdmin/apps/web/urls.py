from django.urls import path, re_path
from .views.user import CreateUser, EditUser, DeleteUser, User, delete_dataset_image
from .views.log import Log, get_log_list
from .views.dashboard import get_dashboard_log_list
from .views.user import get_user_list
from frAdmin.apps.web.views import index
from frAdmin.apps.web.views import Group, EditGroup, RemoveGroup, CreateGroup, get_group_list, ScheduleTime
from frAdmin.apps.web.views.camera import EditCamera, Camera, CreateCamera, RemoveCamera, get_camera_list, SelectCamera
from frAdmin.apps.web.views.modem import EditModem, Modem, CreateModem, RemoveModem, get_modem_list
from frAdmin.apps.web.views.index import stream, get_snapshot
from frAdmin.apps.web.views.schedule_time import EditSchedule, get_schedule_time
from frAdmin.apps.web.views.rasberry import Raspberry, RemoveRaspberry, CreateRaspberry, EditRaspberry, \
    get_raspberry_list
from frAdmin.apps.web.api.authenticate_user import AuthenticateUser
from frAdmin.apps.web.api.last_snapshot import LastSnapShot
from frAdmin.apps.web.views.home import Home
from frAdmin.apps.web.views.login import Login
from frAdmin.apps.web.views.logout import LogOut
from frAdmin.apps.web.views.rasberry import Config, Wifi, reset_raspberry
from frAdmin.apps.web.views.camera import camera_status
from frAdmin.apps.web.views.about import About
from frAdmin.apps.web.views.cam_module import cam

urlpatterns = [
    path('', index, name='index'),
    path('home', Home, name='home'),
    path('login', Login.as_view(), name='login'),
    path('logout', LogOut, name='logout'),
    path('reset_raspberry', reset_raspberry.as_view(), name='reset_raspberry'),
    re_path(r'^user-image/(?P<img_id>(\-?)[0-9]+)/delete$', delete_dataset_image, name='delete_dataset_image'),

    path('user/(?P<user_id>(\-?)[0-9]+)/log/list', get_log_list, name='get_log_list'),
    path('dashboard/list', get_dashboard_log_list, name='get_dashboard_log_list'),
    re_path(r'^user/(?P<id>(\-?)[0-9]+)/log$', Log, name='user_log'),

    path('user', User.as_view(), name='user_list'),
    path('user/list', get_user_list, name='get_user_list'),
    path('user/create', CreateUser.as_view(), name='create_user'),
    re_path(r'^user/(?P<id>(\-?)[0-9]+)$', EditUser.as_view(), name='edit_user'),
    re_path(r'^user/(?P<id>(\-?)[0-9]+)/remove$', DeleteUser.as_view(), name='delete_user'),
    re_path(r'^user/image/(?P<id>(\-?)[0-9]+)/add$', DeleteUser.as_view(), name='add_image'),

    path('stream', stream, name='stream'),
    path('snapshot', get_snapshot, name='get_snapshot'),
    # path('stream', Home, name='stream'),
    # path('snapshot', Home, name='get_snapshot'),

    path('group', Group.as_view(), name='group'),
    path('group/add', CreateGroup.as_view(), name='create-group'),
    path('group/list', get_group_list, name='get-group-list'),
    re_path(r'^group/(?P<id>(\-?)[0-9]+)/edit$', EditGroup.as_view(), name='group-edit'),
    re_path(r'^group/(?P<id>(\-?)[0-9]+)/remove$', RemoveGroup.as_view(), name='group-remove'),

    path('camera', Camera.as_view(), name='camera'),
    path('camera/add', CreateCamera.as_view(), name='create-camera'),
    path('camera/list', get_camera_list, name='get_camera_list'),
    re_path(r'^camera/(?P<id>(\-?)[0-9]+)/edit$', EditCamera.as_view(), name='camera-edit'),
    re_path(r'^camera/(?P<id>(\-?)[0-9]+)/remove$', RemoveCamera.as_view(), name='camera-remove'),
    path('camera/select', SelectCamera.as_view(), name='select_camera'),

    # re_path(r'^group/(?P<id>(\-?)[0-9]+)/get_list_allowed_time$', get_allowed_time, name='get_allowed-time'),

    re_path(r'^group/(?P<id>(\-?)[0-9]+)/getschedule_time$', get_schedule_time, name='get_schedule_time'),
    re_path(r'^group/(?P<id>(\-?)[0-9]+)/edit_schedule$', EditSchedule.as_view(), name='set_weekly_schedule'),
    re_path(r'^group/(?P<id>(\-?)[0-9]+)/schedule_time$', ScheduleTime.as_view(), name='schedule_time'),

    path('raspberry/config', Config.as_view(), name='raspberry_config'),
    path('raspberry/wifi', Wifi.as_view(), name='raspberry_wifi'),

    path('raspberry', Raspberry.as_view(), name='raspberry'),
    path('raspberry/add', CreateRaspberry.as_view(), name='create-raspberry'),
    path('raspberry/list', get_raspberry_list, name='get_raspberry_list'),
    re_path(r'^raspberry/(?P<id>(\-?)[0-9]+)/edit$', EditRaspberry.as_view(), name='raspberry-edit'),
    re_path(r'^raspberry/(?P<id>(\-?)[0-9]+)/modem$', CreateModem.as_view(), name='create_modem'),
    re_path(r'^raspberry/(?P<id>(\-?)[0-9]+)/remove$', RemoveRaspberry.as_view(), name='raspberry-remove'),
    #########################API##########################################################################
    # re_path(r'^api/v1/authenticate/user/(?P<id>.+)$', AuthenticateUser.as_view(), name='api_get_authenticate_user'),
    re_path(r'^group/(?P<id>(\-?)[0-9]+)/getschedule_time$', get_schedule_time, name='get_schedule_time'),
    re_path(r'^group/(?P<id>(\-?)[0-9]+)/edit_schedule$', EditSchedule.as_view(), name='set_weekly_schedule'),
    re_path(r'^group/(?P<id>(\-?)[0-9]+)/schedule_time$', ScheduleTime.as_view(), name='schedule_time'),

    path('api/v1/authenticate/user', AuthenticateUser.as_view(), name='api_get_authenticate_user'),
    # path('api/v1/last_snapshot/user', LastSnapShot.as_view(), name='last_snapshot'),
    path('api/v1/last_snapshot/user', LastSnapShot.as_view(), name='api_get_authenticate_user'),

    path('modem', Modem.as_view(), name='modem'),
    path('modem/list', get_modem_list, name='get_modem_list'),
    re_path(r'^modem/(?P<id>(\-?)[0-9]+)/edit$', EditModem.as_view(), name='edit_modem'),
    re_path(r'^modem/(?P<id>(\-?)[0-9]+)/remove$', RemoveModem.as_view(), name='remove_modem'),

    path('camera/status', camera_status, name='camera_status'),
    path('about', About, name='about_us'),

]

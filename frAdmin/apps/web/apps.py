from django.apps import AppConfig


class webConfig(AppConfig):
    name = 'frAdmin.apps.web'

    def ready(self):
        try:
            from .models.date import Date as DateModel
            from .models.alarms import Alarms as AlarmModel
            from django.contrib.auth.models import User, Group
            from .models.custom_group import Group as MyGroup
            from .models.raspberry import Raspberry
            from .models.camera import Camera

            try:
                if Camera.objects.all().count() == 0:
                    Camera.objects.create(name='camera1', ip='192.168.1.10', username='admin', password='11111')
                    Camera.objects.create(name='camera2', ip='192.168.1.11', username='admin', password='1111')
            except:
                pass

            try:
                if Raspberry.objects.all().count() == 0:
                    Raspberry.objects.create(name='pantos', ip='192.168.1.10', sub_netmask='255.255.255.0',
                                             default_gateway='192.168.1.1', dhcp=False)
            except:
                pass

            try:
                if not User.objects.filter(username='admin').all():
                    User.objects.create_superuser('admin', 'admin@myproject.com', '123456')
            except:
                pass

            try:
                if DateModel.objects.all().count() == 0:
                    DateModel.objects.create(day='شنبه', day_number='0')
                    DateModel.objects.create(day='یک شنبه', day_number='1')
                    DateModel.objects.create(day='دو شنبه', day_number='2')
                    DateModel.objects.create(day='سه شنبه', day_number='3')
                    DateModel.objects.create(day='چهار شنبه', day_number='4')
                    DateModel.objects.create(day='پنج شنبه', day_number='5')
                    DateModel.objects.create(day='جمعه', day_number='6')
            except:
                pass

            try:
                if AlarmModel.objects.all().count() == 0:
                    AlarmModel.objects.create(name='play_voice', title='پخش پیغام صوتی', status=True,
                                              description='پخش پیغام صوتی')
                    AlarmModel.objects.create(name='show_pic', title='نمایش تصویر پروفایل', status=True,
                                              description='نمایش تصویر پروفایل')
                    AlarmModel.objects.create(name='activ_rele1', title='فعال کردن رله ', status=True,
                                              description='فعال کردن رله ')
            except:
                pass

            try:
                admin_group, created = Group.objects.get_or_create(name='admin')
                group_instance = MyGroup.objects.update_or_create(name='admin', active_rele_time=5, group=admin_group)
            except:
                pass

        except Exception as  e:
            print(str(e))
        pass

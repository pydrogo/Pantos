from django.views.generic import TemplateView
from frAdmin.apps.web.utils.set_utils import *
from django.shortcuts import render, get_object_or_404, redirect
from frAdmin.apps.web.models import Group as GroupModel
from frAdmin.apps.web.forms import GroupFrom
from frAdmin.apps.web.models import AuthorizedDay, Date, AuthorizedTime
from django.http import JsonResponse, Http404
from frAdmin.apps.web.models.date import Date
from django.contrib.auth.models import Group as GroupDjango, Permission
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from frAdmin.apps.web.models.alarms import Alarms
from frAdmin.apps.web.models.user_profile import UserProfile

class Group(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        alarm_list = Alarms.objects.all()
        return render(request, 'group/group.html', {'alarm_list': alarm_list})

    def post(self, request, *args, **kwargs):
        pass


class CreateGroup(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('auth.add_group')

    def get(self, request, *args, **kwargs):
        group_form = GroupFrom()
        alarm_list = Alarms.objects.all()
        return render(request, 'group/create.html', {'group_form': group_form, 'alarm_list': alarm_list})

    def post(self, request, *args, **kwargs):
        try:
            alarm_list = Alarms.objects.all()
            form = GroupFrom(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                new_group, created = GroupDjango.objects.get_or_create(name=form.name)
                try:
                    if (request.POST.get('add_userprofile', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='add_userprofile').first())
                    if (request.POST.get('change_userprofile', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='change_userprofile').first())
                    if (request.POST.get('delete_userprofile', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='delete_userprofile').first())

                    if (request.POST.get('add_group', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='add_group').first())
                    if (request.POST.get('change_group', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='change_group').first())
                    if (request.POST.get('delete_group', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='delete_group').first())

                    if (request.POST.get('add_camera', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='add_camera').first())
                    if (request.POST.get('change_camera', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='change_camera').first())
                    if (request.POST.get('delete_camera', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='delete_camera').first())
                    if (request.POST.get('change_authorizedtime', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='change_authorizedtime').first())
                    if (request.POST.get('change_raspberry', 0)):
                        new_group.permissions.add(Permission.objects.filter(codename='change_raspberry').first())
                except:
                    pass
                form.group = new_group
                form.save()
                my_group = GroupModel.objects.get(id=form.id)

                for item in alarm_list:
                    if request.POST.get(item.name, 0):
                        my_group.alarm.add(item)
                    else:
                        a = 1

                msg = "با موفقیت ذخیره شد."
                return redirect('set_weekly_schedule', id=form.id)
            else:
                msg = "خطایی رخ داده است لطفا مجددا تلاش نمایید"
                return redirect('create-group')
        except Exception as e:
            msg = "خطا" + '"' + str(e) + '"'
            return redirect('create-group')


class EditGroup(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('auth.change_group')

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(GroupModel, pk=kwargs['id'])
        django_group = GroupDjango.objects.get(name=group.name)
        permis = list(django_group.permissions.all())
        alarm_list = Alarms.objects.all()
        perm_list = []
        for item in permis:
            perm_list.append(item.codename)

        group_alarm_list = group.alarm.all()
        my_alarms = []
        for alarm in group_alarm_list:
            my_alarms.append(alarm.name)
        if group:
            group_form = GroupFrom(instance=group)
            return render(request, 'group/edit.html',
                          {'group_form': group_form, 'group': group, 'perm_list': perm_list, 'alarm_list': alarm_list,
                           'my_alarms': my_alarms})
        else:
            return Http404

    def post(self, request, *args, **kwargs):
        group = GroupModel.objects.get(pk=kwargs['id'])
        form = GroupFrom(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form = form.save(commit=False)
            new_group, created = GroupDjango.objects.get_or_create(name=form.name)
            new_group.permissions.clear()
            try:
                if (request.POST.get('add_userprofile', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='add_userprofile').first())
                if (request.POST.get('change_userprofile', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='change_userprofile').first())
                if (request.POST.get('delete_userprofile', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='delete_userprofile').first())

                if (request.POST.get('add_group', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='add_group').first())
                if (request.POST.get('change_group', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='change_group').first())
                if (request.POST.get('delete_group', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='delete_group').first())

                if (request.POST.get('add_camera', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='add_camera').first())
                if (request.POST.get('change_camera', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='change_camera').first())
                if (request.POST.get('delete_camera', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='delete_camera').first())
                if (request.POST.get('change_authorizedtime', 0)):
                    new_group.permissions.add(Permission.objects.filter(codename='change_authorizedtime').first())
            except:
                pass
            form.group = new_group
            instance = form.save()

            my_group = GroupModel.objects.get(id=form.id)
            my_group.alarm.clear()
            alarm_list = Alarms.objects.all()
            for item in alarm_list:
                if request.POST.get(item.name, 0) == 'on':
                    my_group.alarm.add(item)
                else:
                    a = 1

            msg = "با موفقیت ذخیره شد."
            return redirect('group')
        else:
            msg = "اطلاعات وارد شده صحیح نمی باشد!"
            return render(request, 'group/edit.html', {'form': form})


class RemoveGroup(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('auth.delete_group')

    def get(self, request, *args, **kwargs):
        try:
            group_instance = get_object_or_404(GroupModel, pk=kwargs['id'])
            group_instance.alarm.clear()
            group_id = group_instance.group_id
            query = 4
            ###############################################################
            userlist = list(UserProfile.objects.filter(group_id=group_id).all().values('user__username'))
            if len(userlist) != 0:
                msg = 'این گروه شامل کاربرانی می باشد!شما مجاز به حذف نمی باشید.'
                alarm_list = Alarms.objects.all()
                return render(request, 'group/group.html', {'alarm_list': alarm_list, 'msg': msg})
            ###############################################################
            GroupDjango.objects.filter(id=group_instance.group_id).delete()
            msg = 'حذف گروه با موفقیت انجام گرفت.'
        except Exception as e:
            msg = 'خطا در حذف گروه!'
        return redirect('group')

    def post(self, request, *args, **kwargs):
        pass


def get_group_list(request):
    search, page, per_page = get_datatable_query(request.GET)
    results, count = GroupModel.objects.search(search, page=page, per_page=per_page)
    return JsonResponse(get_datatable_results(results, count, search), safe=False)


class AllowedTime(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('auth.change_group')

    def get(self, request, *args, **kwargs):
        pk = kwargs['id']
        days = AuthorizedDay.objects.filter(group_id=pk).all().values('group', 'date', 'id')
        result = []
        for item in days:
            auth_time = AuthorizedTime.objects.filter(authorized_day_id=item['id']).all().values('start_hour',
                                                                                                 'end_hour')
            auth_day = Date.objects.filter(id=item['id']).first()
            for item2 in auth_time:
                result.append(
                    {'day': auth_day.day, 'month': auth_day.month, 'year': auth_day.year, 'start': item2['start_hour'],
                     'end': item2['end_hour']})

        return render(request, 'group/allowed_time.html', {'table': result})

    def post(self, request, *args, **kwargs):
        pass

from django.views.generic import TemplateView
from django.http import JsonResponse, Http404
from frAdmin.apps.web.utils.set_utils import *
from django.shortcuts import render, get_object_or_404, redirect
from frAdmin.apps.web.models import Group as Group_model, AuthorizedDay
from frAdmin.apps.web.models import AuthorizedDay
from django.http import JsonResponse, Http404
from frAdmin.apps.web.models.date import Date
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import json


class ScheduleTime(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    def get(self, request, *args, **kwargs):
        group = Group_model.objects.filter(id=kwargs['id']).first()
        return render(request, 'schedule_time/schedule.html', {'group': group})

    def post(self, request, *args, **kwargs):
        pass


class EditSchedule(PermissionRequiredMixin,LoginRequiredMixin,TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.change_authorizedtime')
    def get(self, request, *args, **kwargs):
        time_list_value=[]
        group_id = kwargs['id']
        time_list = AuthorizedDay.objects.filter(group_id=group_id)
        day_list = Date.objects.all()
        if len(day_list)!=len(time_list):
            AuthorizedDay.objects.filter(group_id=group_id).all().delete()
            for item in day_list:
                AuthorizedDay.objects.create(group_id=group_id, date_id=item.id, start='00:00:00',
                                                        end='00:00:00')
        time_list = AuthorizedDay.objects.filter(group_id=group_id)
        for item in time_list:
            time_list_value.append({'day_number': item.date.day_number, 'day': item.date.day, 'start': item.start, 'end': item.end})

        return render(request, 'schedule_time/edite.html', {'time_list':time_list,'day_list':day_list,'time_list_value':time_list_value})


    def post(self, request, *args, **kwargs):
        try:
            post_list = list(request.POST)
            for item in post_list:
                if item.__contains__('start-'):
                    day_number = item.split('-')[1]
                    day_instance = Date.objects.filter(day_number=day_number).first()
                    start = request.POST[item]
                    end = request.POST[item.replace('start', 'end')]
                    if start and end :
                        instance = AuthorizedDay.objects.filter(group_id=request.POST['group_id'],date__day_number=day_number).first()
                        if instance:
                            instance.start=start
                            instance.end=end
                            instance.save()
                        else:
                            instance = AuthorizedDay.objects.create(group_id=request.POST['group_id'],date_id=day_instance.id,start=start,end=end)
                            instance.start = start
                            instance.end = end
                            instance.save()
                else:
                    continue
        except:
            return redirect('schedule_time',id=request.POST['group_id'] )
        return redirect('schedule_time', id=request.POST['group_id'])


def get_schedule_time(request, *args, **kwargs):
    group_id = kwargs['id']
    auth_day = AuthorizedDay.objects.filter(status=1,group_id=group_id).all()
    schedule_list = []
    count=auth_day.count()
    for item in auth_day:
        day = Date.objects.filter(id=item.date_id).first().day
        schedule_list.append({'date': day, 'start': item.start, 'end': item.end, 'id': item.id})

    return JsonResponse(get_datatable_results(schedule_list, count, search=''), safe=False)
from rest_framework.response import Response
from rest_framework.views import APIView
from frAdmin.apps.web.models.authorized_day import AuthorizedDay
from frAdmin.apps.web.models import Date, Group, UserProfile, Alarms, Log
from datetime import datetime, timedelta
import time
import json
import pytz


class AuthenticateUser(APIView):
    def get(self, request, username='', format=None):
        # utc = pytz.UTC
        result = False
        user_name = request.GET['username']
        response = {'username': user_name, 'success': False}
        user_instance = UserProfile.objects.filter(user__username=user_name).first()
        if not user_instance:
            Log.objects.create(action='unknown_user', date=datetime.now(),
                               description=str(response),
                               result=False)
            return Response(response)
        if user_instance.black_list:
            Log.objects.create(username=user_instance.user, action='block_user', date=datetime.now(),
                               description=str(response),
                               result=False)
            return Response(response)

        now = datetime.now()
        last_pass = user_instance.last_pass if user_instance.last_pass else 0

        if last_pass:
            if (last_pass.date() + timedelta(days=1)) < now.date():
                user_instance.counter = 0
                user_instance.save()

        if not user_instance.pass_limitation == 0:  ## pass_limitaion =0  means unlimited
            if user_instance.counter > user_instance.pass_limitation:
                Log.objects.create(username=user_instance.user, action='max_request_exceed', date=datetime.now(),
                                   description=str(response),
                                   result=False)
                return Response(response)

        if user_instance:
            group_instance = user_instance.group
            if group_instance:
                day = datetime.today().weekday() + 2
                if day > 6:
                    day = day - 1
                    day = day % 6
                res = AuthorizedDay.objects.filter(group_id=group_instance.id, date__day_number=day).first()
                if res:
                    now = str(datetime.now().time()).split('.')[0]
                    print(now)
                    print(res.start)
                    print(res.end)
                    if res.start < now and res.end > now:
                        user_instance.counter += 1
                        user_instance.last_pass = datetime.now()
                        user_instance.save()
                        result = True
                        response['success'] = True
                        mygroup = Group.objects.filter(id=user_instance.group.group.id).first()
                        myalarm = list(mygroup.alarm.all())
                        alarm_list = Alarms.objects.all()
                        response['alarms'] = []
                        for alarm in alarm_list:
                            if alarm in myalarm:
                                if alarm.name == 'play_voice':
                                    voice_url = str(mygroup.welcome_voice)
                                    response['alarms'].append({alarm.name: True})
                                    response['alarms'].append({'voice_url': voice_url})
                                elif alarm.name == 'activ_rele1':
                                    response['alarms'].append({alarm.name: True})
                                    response['alarms'].append({alarm.name + '_time': mygroup.active_rele_time})
                                else:
                                    response['alarms'].append({alarm.name: True})
                            else:
                                response['alarms'].append({alarm.name: False})
                        Log.objects.create(username=user_instance.user, action='ok', date=datetime.now(),
                                           description=str(response),
                                           result=True)
                    else:
                        Log.objects.create(username=user_instance.user, action='unauthorized_time', date=datetime.now(),
                                           description=str(response),
                                           result=True)
        return Response(response)

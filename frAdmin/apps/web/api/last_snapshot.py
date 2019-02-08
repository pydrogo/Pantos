from rest_framework.response import Response
from rest_framework.views import APIView
from frAdmin.apps.web.models.authorized_day import AuthorizedDay
from frAdmin.apps.web.models import Date, Group, UserProfile, Alarms, Log
from datetime import datetime, timedelta
import time
import pytz


class LastSnapShot(APIView):
    def get(self, request, username='', format=None):
        pass
        # return Response(response)

    def post(self, request, **kwargs):
        try:
            response = {'success': False}
            user_name = request.POST['user_name']
            path = request.POST['path']
            user_instance = UserProfile.objects.filter(user__username=user_name).first()
            if user_instance:
                user_instance.last_snapshot = path
                user_instance.save()
                response['success'] = True
            return Response(response)
        except:
            return Response({'success': False})

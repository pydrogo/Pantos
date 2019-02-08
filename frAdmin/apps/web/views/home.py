from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from frAdmin.apps.web.models.user_profile import UserProfile
from frAdmin.apps.web.models.logs import Log as log_model
import datetime


@login_required(login_url='login')
def Home(request):
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 00, 00)
    today_pass = log_model.objects.filter(date__gte=today, action='ok').all()
    blocked_pass = log_model.objects.filter(date__gte=today, action='block_user').all()
    unauthorized_user = log_model.objects.filter(date__gte=today, action='unauthorized_time').all()
    return render(request, 'home/home.html', {'today_pass': today_pass.count(), 'blocked_pass': blocked_pass.count(),
                                              'unauthorized_user': unauthorized_user.count()})


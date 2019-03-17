from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from frAdmin.apps.web.forms.log_form import LogForm
from frAdmin.apps.web.utils.set_utils import *
from frAdmin.apps.web.models.logs import Log as log_model
from frAdmin.apps.web.models.user_profile import UserProfile


def Log(request, *args, **kwargs):
    userprofile_instance = get_object_or_404(UserProfile, pk=kwargs['id'])
    log_form = LogForm(instance=userprofile_instance)
    return render(request, 'log/log.html', {'log_form': log_form, 'user_id': kwargs.get('id', 0)})


def get_log_list(request, user_id):
    query = log_model.objects.filter(username__UserProfile__id=user_id)
    search, page, per_page = get_datatable_query(request.GET)
    count = query.count()
    start_row = int(per_page * page)
    query = query[start_row:start_row + per_page]
    results = list(
        query.values('id', 'date', 'description', 'action', 'result', 'username__UserProfile', 'username__username'))
    return JsonResponse(get_datatable_results(results, count, search), safe=False)

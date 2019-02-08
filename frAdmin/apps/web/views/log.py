from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from frAdmin.apps.web.forms.log_form import LogForm
from frAdmin.apps.web.utils.set_utils import *
from frAdmin.apps.web.models.logs import Log as log_model
from frAdmin.apps.web.models.user_profile import UserProfile


def Log(request, *args, **kwargs):
    userprofile_instance = get_object_or_404(UserProfile, pk=kwargs['id'])
    log_form = LogForm(instance=userprofile_instance)
    return render(request, 'log/log.html', {'log_form': log_form})


def get_log_list(request):
    search, page, per_page = get_datatable_query(request.GET)
    results, count = log_model.objects.search(search, page=page, per_page=per_page)
    return JsonResponse(get_datatable_results(results, count, search), safe=False)

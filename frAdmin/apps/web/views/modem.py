from django.views.generic import TemplateView
from frAdmin.apps.web.utils.set_utils import *
from django.shortcuts import render, get_object_or_404, redirect
from frAdmin.apps.web.forms import ModemForm
from django.http import JsonResponse, Http404
from frAdmin.apps.web.models import Modem as Modem_model
from frAdmin.apps.web.models import Raspberry as Raspberry_model
import requests


class Modem(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'modem/modem.html')


class CreateModem(TemplateView):
    def get(self, request, *args, **kwargs):
        modem = get_object_or_404(Raspberry_model, pk=kwargs['id'])
        if (modem.dhcp == True):
            raspberry = Raspberry_model.objects.filter(pk=kwargs['id']).first()
            raspberry_name = raspberry.name
            if modem:
                modem_form = ModemForm(instance=modem)
                return render(request, 'modem/create.html',
                              {'modem_form': modem_form, 'raspberry_name': raspberry_name, 'raspberry': raspberry})
            else:
                return Http404
        else:
            msg = 'گزینه dhcp برای این رزبری فعال نگردیده است'
            return render(request, 'raspberry/rasberry.html', {'msg': msg})

    def post(self, request, *args, **kwargs):
        try:
            form = ModemForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                form.raspberry = request.POST['raspberry']
                form.save()
                msg = "با موفقیت ذخیره شد."
                return redirect('raspberry')
            else:
                msg = "خطایی رخ داده است لطفا مجددا تلاش نمایید"
                return redirect('raspberry')
        except Exception as e:
            msg = "خطا" + '"' + str(e) + '"'
            return redirect('raspberry')


class EditModem(TemplateView):
    def get(self, request, *args, **kwargs):
        modem = get_object_or_404(Modem_model, pk=kwargs['id'])
        raspberry = Modem_model.objects.filter(pk=kwargs['id']).first()
        raspberry_name = raspberry.raspberry.name
        if modem:
            modem_form = ModemForm(instance=modem)
            return render(request, 'modem/edit.html',
                          {'modem_form': modem_form, 'raspberry_name': raspberry_name, 'raspberry': raspberry})
        else:
            return Http404

    def post(self, request, *args, **kwargs):
        modem = Modem_model.objects.get(pk=kwargs['id'])
        form = ModemForm(request.POST, instance=modem)
        if form.is_valid():
            instance = form.save(commit=False)
            form.raspberry = request.POST['raspberry']
            form.save()
            return redirect('modem')
        else:
            return render(request, 'modem/edit.html', {'form': form})


class RemoveModem(TemplateView):
    def get(self, request, *args, **kwargs):
        modem_instance = get_object_or_404(Modem_model, pk=kwargs['id'])
        modem_instance.delete()
        return render(request, 'modem/modem.html')


def get_modem_list(request):
    search, page, per_page = get_datatable_query(request.GET)
    results, count = Modem_model.objects.search(search, page=page, per_page=per_page)
    return JsonResponse(get_datatable_results(results, count, search), safe=False)

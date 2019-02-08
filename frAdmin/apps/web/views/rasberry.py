from django.views.generic import TemplateView
from frAdmin.apps.web.utils.set_utils import *
from django.shortcuts import render, get_object_or_404, redirect
from frAdmin.apps.web.forms import RaspberryForm
from django.http import JsonResponse, Http404
from frAdmin.apps.web.models import Raspberry as Raspberry_model
import requests
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import json


class Config(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.change_raspberry')

    def get(self, request, *args, **kwargs):
        config = Raspberry_model.objects.first()
        form = None
        if config:
            form = RaspberryForm(instance=config)
        else:
            form = RaspberryForm()
        return render(request, 'raspberry/config.html', {'config_form': form})

    def post(self, request, *args, **kwargs):
        try:
            previus_config = Raspberry_model.objects.first()
            previous_username = previus_config.name
            previous_subnet_mask = previus_config.sub_netmask
            previous_ip = previus_config.ip
            previous_getway = previus_config.default_gateway
            config = Raspberry_model.objects.first()

            if (config.dhcp == True and request.POST.get('dhcp', 0) == 'on'):
                msg = "DHCP  قبلا فعال گردیده است . نمیتوانید مجددا آن را فعال کنید."
                config = Raspberry_model.objects.first()
                form = RaspberryForm(instance=config)
                return render(request, 'raspberry/config.html', {'config_form': form, 'msg': msg})
            form = RaspberryForm(request.POST, request.FILES, instance=config)
            if form.is_valid():
                data = {}
                dhcp = form.cleaned_data.get('dhcp', 0)
                if dhcp:
                    data = {
                        'previous_username': previous_username,
                        'new_username': form.cleaned_data['name'],
                        'dhcp': True,
                    }
                else:
                    data = {
                        'previous_username': previous_username,
                        'new_username': form.cleaned_data['name'],
                        'dhcp': False,
                        'previous_ip': previous_ip,
                        'previous_subnet_mask': previous_subnet_mask,
                        'previous_getway': previous_getway,
                        'new_ip': form.cleaned_data['ip'],
                        'new_getway': form.cleaned_data['default_gateway'],
                        'new_subnet_mask': form.cleaned_data['sub_netmask'],
                    }
                if request.POST.get('play_video_intro', 0) and (
                        form.fields.get('play_video_intro', 0) or config.play_video_intro):
                    data['video_introduction'] = True
                else:
                    data['video_introduction'] = False
                if request.POST.get('unkown_person') == 'on' and request.POST.get('ftp_path', '') != '':
                    data['unkown_persons'] = True
                    if form.cleaned_data.get('ftp_path', False) != None:
                        data['ftp_path'] = form.cleaned_data.get('ftp_path', False)
                    else:
                        data['ftp_path'] = 'defuat directory'  ####
                    if form.cleaned_data.get('ftp_username', False) != None:
                        data['ftp_username'] = form.cleaned_data.get('ftp_username', False)
                    else:
                        data['ftp_username'] = ''
                    if form.cleaned_data.get('ftp_password', False) != None:
                        data['ftp_password'] = form.cleaned_data.get('ftp_password', False)
                    else:
                        data['ftp_password'] = ''
                else:
                    data['unkown_persons'] = False
                res = requests.post('http://localhost:8888/change_raspberry', data=json.dumps(data))
                if res.status_code == 200:
                    raspb = form.save(commit=False)
                    if (data['unkown_persons'] == False):
                        raspb.unkown_person = False
                        raspb.save()
                    msg = "با موفقیت ارسال شد"
                    return render(request, 'raspberry/config.html',
                                  {'config_form': RaspberryForm(instance=config), 'msg': msg})
                else:
                    msg = 'خطا در اتصال به رزبری'
                    return render(request, 'raspberry/config.html', {'config_form': form, 'msg': msg})
        except Exception as e:
            config = Raspberry_model.objects.first()
            form = None
            if config:
                form = RaspberryForm(instance=config)
            else:
                form = RaspberryForm()
            return render(request, 'raspberry/config.html',
                          {'config_form': form, 'error': 'مشکلی پیش آمده است لطفا دوباره تلاش نمایید' + str(e)})


class Wifi(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.change_raspberry')

    def get(self, request, *args, **kwargs):
        res = requests.get('http://localhost:8888/wifi/status', verify=False)
        data = res.json()
        return render(request, 'raspberry/wifi.html', {'wifi_status': data})

    def post(self, request, *args, **kwargs):
        try:
            wifi_turn_on = request.POST.get('wifi_turn_on', 0)
            if wifi_turn_on == '1':
                data = {'wifi_turn_on': True}
                res = requests.post('http://localhost:8888/wifi', data=json.dumps(data))
                if res.status_code == 200:
                    msg = 'با موفقیت ارسال شد'
                    return render(request, 'raspberry/wifi.html', {'msg': msg})
                else:
                    msg = 'خطا در اتصال به رزبری'
                    return render(request, 'raspberry/wifi.html', {'msg': msg})
            ################################################################################
            wifi_password = request.POST.get('wifi_password', 0)
            ssid = request.POST.get('ssid', 0)
            data = {
                'ssid': ssid,
                'password': wifi_password,
            }
            res = requests.post('http://localhost:8888/wifi', data=json.dumps(data))
            if res.status_code == 200:
                # if res.data['status':success]
                # else sfail add camera
                msg = 'با موفقیت ارسال شد'
                return render(request, 'raspberry/wifi.html', {'msg': msg})
            else:
                msg = 'خطا در اتصال به رزبری'
                return render(request, 'raspberry/wifi.html', {'msg': msg})
        except:
            pass

        return redirect('raspberry_wifi')


class reset_raspberry(TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.change_camera')

    def get(self, request, *args, **kwargs):
        try:
            config = Raspberry_model.objects.first()
            if config:
                form = RaspberryForm(instance=config)
            else:
                form = RaspberryForm()
            res = requests.post('http://localhost:8888/reset_raspberry')
            if res.status_code == 200:
                msg = "دستگاه با موفقیت راه اندازی شد."
                return render(request, 'raspberry/config.html',
                              {'config_form': form, 'msg': msg})
            else:
                msg = 'خطا در اتصال به رزبری'
                return render(request, 'raspberry/config.html', {'config_form': form, 'msg': msg})
        except:
            return render(request, 'raspberry/config.html',
                          {'config_form': RaspberryForm, 'msg': 'خطایی رخ داده است!لطفا صفحه را رفرش نمایید.'})

    def post(self, request, *args, **kwargs):
        pass


########################################################################################################################

class Raspberry(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'raspberry/rasberry.html')


class CreateRaspberry(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
        # raspberry_form = RaspberryForm()
        # return render(request, 'raspberry/create.html', {'raspberry_form': raspberry_form})

    def post(self, request, *args, **kwargs):
        pass
        # try:
        #     form = RaspberryForm(request.POST)
        #     if form.is_valid():
        #         instance = form.save()
        #         msg = "با موفقیت ذخیره شد."
        #         return redirect('raspberry')
        #     else:
        #         msg = "خطایی رخ داده است لطفا مجددا تلاش نمایید"
        #         return redirect('create-raspberry')
        # except Exception as e:
        #     msg = "خطا" + '"' + str(e) + '"'
        #     return redirect('create-raspberry')


class EditRaspberry(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
        # raspberry = get_object_or_404(Raspberry_model, pk=kwargs['id'])
        # if raspberry:
        #     raspberry_form = RaspberryForm(instance=raspberry)
        #     return render(request, 'raspberry/edit.html', {'raspberry_form': raspberry_form, 'raspberry': raspberry})
        # else:
        #     return Http404

    def post(self, request, *args, **kwargs):
        pass
        # raspberry = Raspberry_model.objects.get(pk=kwargs['id'])
        # raspberry_instanse = Raspberry_model.objects.filter(pk=kwargs['id']).first()
        # form = RaspberryForm(request.POST, instance=raspberry)
        # if form.is_valid():
        #     form.save()
        #     if (form.cleaned_data['dhcp'] != raspberry_instanse.dhcp):
        #         model_instanse = Modem_model.objects.filter(raspberry__name=raspberry_instanse.name).delete()
        #     return redirect('raspberry')
        # else:
        #     return render(request, 'raspberry/edit.html', {'form': form})
        #
        # # msg =''
        # # camera = Camera_model.objects.get(pk=kwargs['id'])
        # # form = CameraForm(request.POST, instance=camera)
        # # previous_ip = camera.ip
        # # try:
        # #     if form.is_valid():
        # #         form.save()
        # #     res = requests.get(parameter.chang_ip_url,
        # #                        data={'change_ip': {'previous_ip': previous_ip, 'new_ip': form.ip}})
        # #     if res.status_code == '200' :
        # #         msg = 'درخواست تغییر آی پی با موفقیت صورت گرفت.'
        # #     elif res.status_code =='400':
        # #         msg = 'درخواست تغییر آی پی با خطا مواجه شد.(خطا در دریافت پاسخ از رزبری)'
        # # except Exception as e:
        # #     msg = 'درخواست تغییر آی پی با خطا مواجه شد.'
        # #     camera = Camera_model.objects.get(pk=kwargs['id'])
        # #     camera.ip = previous_ip
        # #     camera.save()


class RemoveRaspberry(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
        # raspberry_instance = get_object_or_404(Raspberry_model, pk=kwargs['id'])
        # raspberry_instance.delete()
        # return render(request, 'raspberry/rasberry.html')


def get_raspberry_list(request):
    search, page, per_page = get_datatable_query(request.GET)
    results, count = Raspberry_model.objects.search(search, page=page, per_page=per_page)
    return JsonResponse(get_datatable_results(results, count, search), safe=False)

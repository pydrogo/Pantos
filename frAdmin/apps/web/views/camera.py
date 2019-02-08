from django.views.generic import TemplateView
from frAdmin.apps.web.utils.set_utils import *
from django.shortcuts import render, get_object_or_404, redirect
from frAdmin.apps.web.forms import CameraForm
from django.http import JsonResponse, Http404
from frAdmin.apps.web.models import Camera as CameraModel
from frAdmin.apps.web.models.raspberry import Raspberry
import requests
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import json



class Camera(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request, *args, **kwargs):
        return render(request, 'camera/camera.html')


class CreateCamera(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.add_camera')

    def get(self, request, *args, **kwargs):
        camera_form = CameraForm()
        return render(request, 'camera/create.html', {'camera_form': camera_form})

    def post(self, request, *args, **kwargs):
        try:
            rasspberry = Raspberry.objects.first()
            form = CameraForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('camera')
            else:
                msg = "خطا در اعتبار سنجی فرم !"
                return render(request, 'camera/create.html', {'camera_form': form, 'msg': msg})
        except Exception as e:
            msg = "خطا" + '"' + str(e) + '"'
            return redirect('create-camera')


class EditCamera(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.change_camera')

    def get(self, request, *args, **kwargs):
        camera = get_object_or_404(CameraModel, pk=kwargs['id'])
        if camera:
            camera_form = CameraForm(instance=camera)
            return render(request, 'camera/edit.html', {'camera_form': camera_form, 'camera': camera})
        else:
            return Http404

    def post(self, request, *args, **kwargs):
        rasspberry = Raspberry.objects.first()
        camera = CameraModel.objects.get(pk=kwargs['id'])
        previous_camera = CameraModel.objects.get(pk=kwargs['id'])
        form = CameraForm(request.POST, instance=camera)
        try:
            if form.is_valid():
                form.save()
                return redirect('camera')
            else:
                msg = "خطا در تکمیل اطلاعات!"
                return render(request, 'camera/edit.html', {'camera_form': form, 'msg': msg})
        except Exception as e:
            msg = 'درخواست تغییر آی پی با خطا مواجه شد.'
            return render(request, 'camera/edit.html', {'camera_form': form, 'msg': msg})


class RemoveCamera(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.delete_camera')

    def get(self, request, *args, **kwargs):
        group_instance = get_object_or_404(CameraModel, pk=kwargs['id'])
        group_instance.delete()
        return render(request, 'camera/camera.html')


class SelectCamera(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.delete_camera')

    def get(self, request, *args, **kwargs):
        camera_list = CameraModel.objects.all()
        return render(request, 'camera/select_camera.html', {'camera_list': camera_list})

    def post(self, request, *args, **kwargs):
        camera_list = CameraModel.objects.all()
        cam1 = None
        cam2 = None
        count = 0
        json_data = {
            'camera1': {},
            'camera2': {},
        }
        for item in camera_list:
            if item.is_active:
                item.is_active = False
                item.save()
            if (request.POST.get('check-' + str(item.id), 0)):
                if (count == 0):
                    json_data['camera1'] = {
                        'new_ip': item.ip,
                        'new_username': item.username,
                        'new_password': item.password,
                        'new_name': item.name,
                    }
                    count += 1
                    item.is_active = True
                    item.save()
                    cam1 = item
                else:
                    json_data['camera2'] = {
                        'new_ip': item.ip,
                        'new_username': item.username,
                        'new_password': item.password,
                        'new_name': item.name,
                    }
                    item.is_active = True
                    item.save()
                    cam2 = item
                    break

        res = ''
        try:
            res = requests.post('http://localhost:8888/camera', data=json.dumps(json_data))
            if res.status_code == 200:
                recive_data = res.json()
                cam1_status = recive_data[0].get('cam1', False)
                cam2_status = recive_data[1].get('cam2', False)
                if cam1:
                    cam1.is_active = cam1_status
                    cam1.save()
                if cam2:
                    cam2.is_active = cam2_status
                    cam2.save()
                if (cam1_status):
                    cam1_status = " فعال "
                else:
                    cam1_status = " غیر فعال "
                if (cam2_status):
                    cam2_status = " فعال "
                else:
                    cam2_status = " غیر فعال "
                msg = "دوربین یک " + cam1_status + " -- " + "دوربین دو  " + cam2_status
                return render(request, 'camera/select_camera.html', {'camera_list': camera_list, 'msg': msg})
            else:
                msg = 'خطا در اتصال به رزبری، لطفا مجددا تلاش کنید.'
                return render(request, 'camera/select_camera.html', {'camera_list': camera_list, 'msg': msg})
        except Exception as e:
            msg = 'خطایی رخ داده است ' + str(e)
            camera_list = CameraModel.objects.all()
            return render(request, 'camera/select_camera.html', {'camera_list': camera_list, 'msg': msg})


def get_camera_list(request):
    search, page, per_page = get_datatable_query(request.GET)
    results, count = CameraModel.objects.search(search, page=page, per_page=per_page)
    return JsonResponse(get_datatable_results(results, count, search), safe=False)


def camera_status(request):
    cam1_id = int(request.GET.get('cam1', -1))
    cam2_id = int(request.GET.get('cam2', -1))

    cam1 = CameraModel.objects.filter(id=int(cam1_id)).first()
    cam2 = CameraModel.objects.filter(id=int(cam2_id)).first()
    json_data = {}

    try:
        if cam1:
            json_data['camera1'] = {
                'new_ip': cam1.ip,
                'new_username': cam1.username,
                'new_password': cam1.password,
                'new_name': cam1.name,

            }
        if cam2:
            json_data['camera2'] = {
                'new_ip': cam2.ip,
                'new_username': cam2.username,
                'new_password': cam2.password,
                'new_name': cam2.name,

            }
    except Exception as e:
        print(str(e))
    if json_data:
        res = requests.get('http://localhost:8888/camera/status', data=json.dumps(json_data))
        if res.status_code == 200:
            recive_data = res.json()
            cam1_status = recive_data.get('cam1', 0)
            cam2_status = recive_data.get('cam2', 0)
            name1 = recive_data.get('name1', 0)
            name2 = recive_data.get('name2', 0)
            flag = True
            ajax_data = {}
            if cam1_id != -1 and cam1_status:
                flag = True
            else:
                flag = False

            if cam2_id != -1 and cam2_status and flag:
                flag = True
            else:
                if cam2_id != -1:
                    flag = False

            if cam1_id != -1:
                cam1_msg = 'فعال سازی دوربین {} با موفقیت انجام شد.'.format(
                    name1) if cam1_status else 'خطا در فعالسازی دوربین {}'.format(name1)
            else:
                cam1_msg = ''

            if cam2_id != -1:
                cam2_msg = 'فعال سازی دوربین {} با موفقیت انجام شد.'.format(
                    name2) if cam2_status else 'خطا در فعالسازی دوربین {}'.format(name2)
            else:
                cam2_msg = ''

            ajax_data['flag'] = flag
            ajax_data['msg'] = '{},{}'.format(cam1_msg, cam2_msg)

            return JsonResponse(ajax_data)
        else:
            return JsonResponse({'flag': False, 'msg': 'خطا در اتصال به رزبری!'})

import base64
import uuid
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from requests import request

from frAdmin.apps.web.forms.user_profile import UserProfileForm
from frAdmin.apps.web.forms.user_image import UserImageForm
from frAdmin.apps.web.forms.user import UserForm
from frAdmin.apps.web.utils.set_utils import *
from django.contrib.auth.models import User as user_model
from frAdmin.apps.web.models.user_profile import UserProfile as userprofile_model
from frAdmin.apps.web.models.image import UserImage as userimage_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group as GroupDjango
from frAdmin.apps.web.models.camera import Camera as CameraModel
import requests
import json
import os, shutil
from django.conf import settings
import re


class User(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.add_userprofile')

    def get(self, request, *args, **kwargs):
        return render(request, 'user/user.html')

    def post(self, request, *args, **kwargs):
        return render(request, 'user/user.html')


class CreateUser(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.add_userprofile')

    def get(self, request, *args, **kwargs):
        userform = UserForm()
        userprofileform = UserProfileForm()
        imageform = UserImageForm()
        camera_list = CameraModel.objects.filter(is_active=True)
        return render(request, 'user/create_user.html',
                      {'userform': userform, 'imageform': imageform, 'userprofileform': userprofileform,
                       'camera_list': camera_list})

    def post(self, request, *args, **kwargs):
        try:
            msg = ''
            user_block = False
            try:
                user_block = request.POST.get('black_list', 'off')
                if user_block == 'on':
                    user_block = True
                else:
                    user_block = False
            except:
                user_block = False
            if request.POST.get('is_active', 0):
                is_active = True
            else:
                is_active = False
            user_row = 1
            ni_validation = request.POST.get('username', '')
            validation_int = int(ni_validation)
            if (isinstance(validation_int, int) != False):
                p = re.compile('^[0][1-9]\d{9}$|^[1-9]\d{9}$')
                if (p.match(ni_validation) != None):
                    pass
                else:
                    userform = UserForm(request.POST, request.FILES)
                    userprofileform = UserProfileForm(request.POST, request.FILES)
                    imageform = UserImageForm(request.POST, request.FILES)
                    camera_list = CameraModel.objects.filter(is_active=True)
                    return render(request, 'user/create_user.html',
                                  {'user_row': user_row, 'userform': userform, 'imageform': imageform,
                                   'userprofileform': userprofileform,
                                   'camera_list': camera_list})
            create_user, created = user_model.objects.update_or_create(username=request.POST['username'],
                                                                       first_name=request.POST['first_name'],
                                                                       last_name=request.POST['last_name'],
                                                                       email=request.POST['email'],
                                                                       )
            create_user.set_password(request.POST['password'])
            create_user.save()

            user_id = create_user.id
            user_instance = user_model.objects.get(pk=user_id)
            if request.FILES.get('image_profile', 0) and request.FILES['image_profile'] != '':
                create_userprofile, created = userprofile_model.objects.update_or_create(user_id=user_id,
                                                                                         unit=request.POST['unit'],
                                                                                         group_id=request.POST['group'],
                                                                                         mobile=request.POST['mobile'],
                                                                                         black_list=user_block,
                                                                                         pass_limitation=request.POST[
                                                                                             'pass_limitation'],
                                                                                         image_profile=request.FILES[
                                                                                             'image_profile'])

            else:
                create_userprofile, created = userprofile_model.objects.update_or_create(user_id=user_id,
                                                                                         unit=request.POST['unit'],
                                                                                         group_id=request.POST['group'],
                                                                                         pass_limitation=request.POST[
                                                                                             'pass_limitation'],
                                                                                         black_list=user_block,
                                                                                         mobile=request.POST['mobile'])

            group = GroupDjango.objects.get(pk=request.POST['group'])
            group.user_set.add(create_user)

            userprofile_id = create_userprofile.id
            userprofile_instance = userprofile_model.objects.get(pk=userprofile_id)
            for item in request.FILES.getlist('profile_image'):
                userimage_model.objects.create(user=userprofile_instance,
                                               profile_image=item)
            stream_row_id = request.POST.get('row_id', 0)
            if stream_row_id != 0:
                for item in range(0, int(stream_row_id) + 1):
                    if request.POST.get('stream_image' + str(item), None):
                        user_img = userimage_model(user=userprofile_instance)
                        filename = "%s.%s" % (uuid.uuid4(), 'jpg')
                        user_img.profile_image.save(name=filename,
                                                    content=ContentFile(
                                                        base64.b64decode(
                                                            request.POST.get('stream_image' + str(item), '')),
                                                        name=filename))
                        user_img.save()
            ####### send api to encode image  ############################################################
            res = requests.post('http://localhost:8888/encoding',
                                data=json.dumps({'encoding': True, 'username': create_user.username, 'prof': 'Added'}))
            if res.status_code == 200:
                msg = 'کد گزاری تصاویر با موفیقت انجام شد'
            else:
                msg = 'خطا در اتصال به رزبری'
            ###################################################################
        except Exception as ex:
            print(str(ex))
            # if (user_model.objects.filter(username=request.POST['username']).first()):
            #     user_model.objects.filter(username=request.POST['username']).delete()
        return redirect('user_list')


class EditUser(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.change_userprofile')

    def get(self, request, *args, **kwargs):
        userprofile_instance = get_object_or_404(userprofile_model, pk=kwargs['id'])
        user_id = userprofile_instance.user_id
        user = user_model.objects.get(pk=user_id)
        user_username = user.username
        imageprofile_instance = userimage_model(user=userprofile_instance)
        camera_list = CameraModel.objects.filter(is_active=True)
        if user:
            user_instance_form = UserForm(instance=user)
            userprofile_instance_form = UserProfileForm(instance=userprofile_instance)
            image_instance_form = UserImageForm(instance=imageprofile_instance)
            image_url = userimage_model.objects.filter(user_id=userprofile_instance).all()
            profile_image_url = userprofile_model.objects.filter(pk=kwargs['id']).all()
            return render(request, 'user/edit_user.html', {'user_instance_form': user_instance_form,
                                                           'user_username': user_username,
                                                           'userprofile_instance_form': userprofile_instance_form,
                                                           'image_instance_form': image_instance_form,
                                                           'image_url': image_url,
                                                           'profile_image_url': profile_image_url,
                                                           'camera_list': camera_list})
        else:
            return render(request, 'user/user.html')

    def post(self, request, *args, **kwargs):
        is_active = True
        user_block = False
        try:
            user_block = request.POST.get('black_list', 'off')
            if user_block == 'on':
                user_block = True
            else:
                user_block = False
        except:
            user_block = False
        try:
            if request.POST.get('is_active', 0):
                is_active = True
        except:
            is_active = False
        user_row = 1
        ni_validation = request.POST.get('username', '')
        validation_int = int(ni_validation)
        if (isinstance(validation_int, int) != False):
            p = re.compile('^[0][1-9]\d{9}$|^[1-9]\d{9}$')
            if (p.match(ni_validation) != None):
                pass
            else:
                userform = UserForm(request.POST, request.FILES)
                userprofileform = UserProfileForm(request.POST, request.FILES)
                imageform = UserImageForm(request.POST, request.FILES)
                camera_list = CameraModel.objects.filter(is_active=True)
                return render(request, 'user/create_user.html',
                              {'user_row': user_row, 'userform': userform, 'imageform': imageform,
                               'userprofileform': userprofileform,
                               'camera_list': camera_list})
        try:
            userprofile_instance = get_object_or_404(userprofile_model, pk=kwargs['id'])
            user_id = userprofile_instance.user_id
            user = user_model.objects.get(pk=user_id)
            # userprofile_id = userprofile_instance.id
            imageprofile_instance = userimage_model(user=userprofile_instance)
            if user:
                if request.POST.get('password', 0) and request.POST['password'] != '':
                    create_user = user_model.objects.filter(pk=user_id).update(username=request.POST['username'],
                                                                               first_name=request.POST['first_name'],
                                                                               last_name=request.POST['last_name'],
                                                                               email=request.POST['email'],
                                                                               password=request.POST['password'])
                else:
                    # passw = user_model.objects.filter(pk=user_id).first().password
                    create_user = user_model.objects.filter(pk=user_id).update(username=request.POST['username'],
                                                                               first_name=request.POST['first_name'],
                                                                               last_name=request.POST['last_name'],
                                                                               email=request.POST['email'],
                                                                               )
                if request.FILES.get('image_profile', 0) and request.FILES['image_profile'] != '':
                    create_userprofile = userprofile_model.objects.filter(pk=kwargs['id']).update(user_id=user_id,
                                                                                                  unit=request.POST[
                                                                                                      'unit'],
                                                                                                  group_id=request.POST[
                                                                                                      'group'],
                                                                                                  mobile=request.POST[
                                                                                                      'mobile'],
                                                                                                  pass_limitation=
                                                                                                  request.POST[
                                                                                                      'pass_limitation'],
                                                                                                  black_list=user_block,
                                                                                                  image_profile=
                                                                                                  request.FILES[
                                                                                                      'image_profile'])
                else:
                    create_userprofile = userprofile_model.objects.filter(pk=kwargs['id']).update(user_id=user_id,
                                                                                                  unit=request.POST[
                                                                                                      'unit'],
                                                                                                  group_id=request.POST[
                                                                                                      'group'],
                                                                                                  black_list=user_block,
                                                                                                  pass_limitation=
                                                                                                  request.POST[
                                                                                                      'pass_limitation'],
                                                                                                  mobile=request.POST[
                                                                                                      'mobile'])

                for item in request.FILES.getlist('profile_image'):
                    # userimage_model.objects.filter(user=userprofile_instance).delete()
                    userimage_model.objects.create(user=userprofile_instance,
                                                   profile_image=item)
                stream_row_id = request.POST.get('row_id', 0)
                if stream_row_id != 0:
                    for item in range(0, int(stream_row_id) + 1):
                        if request.POST.get('stream_image' + str(item), None):
                            user_img = userimage_model(user=userprofile_instance)
                            filename = "%s.%s" % (uuid.uuid4(), 'jpg')
                            user_img.profile_image.save(name=filename,
                                                        content=ContentFile(
                                                            base64.b64decode(
                                                                request.POST.get('stream_image' + str(item), '')),
                                                            name=filename), save=True)
                            user_img.save()
                if request.FILES.getlist('profile_image'):
                    ####### send api to encode image  ############################################################
                    res = requests.post('http://localhost:8888/encoding', data=json.dumps(
                        {'encoding': True, 'username': userprofile_instance.user.username, 'prof': 'Edited'}))
                    if res.status_code == 200:
                        msg = 'کد گزاری تصاویر با موفیقت انجام شد'
                    else:
                        msg = 'خطا در اتصال به رزبری'
                    ####### send api to encode image  ############################################################
                if request.FILES.get('stream_image', 0) and request.FILES['stream_image'] != '':
                    userimage_model.objects.filter(user_id=kwargs['id']).update(
                        profile_image=request.FILES['stream_image'])
                    ####### send api to encode image  ############################################################
                    res = requests.post('http://localhost:8888/encoding', data=json.dumps(
                        {'encoding': True, 'username': userprofile_instance.user.username, 'prof': 'Edited'}))
                    if res.status_code == 200:
                        msg = 'کد گزاری تصاویر با موفیقت انجام شد'
                    else:
                        msg = 'خطا در اتصال به رزبری'
                    ####### send api to encode image  ############################################################
        except Exception as ex:
            print(str(ex))
            pass
        return redirect('user_list')


class DeleteUser(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'login'
    permission_required = ('web.delete_userprofile')

    def get(self, request, *args, **kwargs):
        try:
            userprofile_instance = get_object_or_404(userprofile_model, id=kwargs['id'])
            username = userprofile_instance.user.username
            try:
                base_dir = settings.MEDIA_ROOT.replace('\\', '/')
                dataset_dir = base_dir + "/fr_pics/dataset/{}".format(str(username))
                shutil.rmtree(dataset_dir)
                os.remove(base_dir + "fr_pics/profile_pic/" + str(username))
            except Exception as e:
                print(str(e))
            user_model.objects.filter(username=username).delete()
            ####### send api to encode image  ############################################################
            res = requests.post('http://localhost:8888/encoding',
                                data=json.dumps({'encoding': True, 'username': username, 'prof': 'Deleted'}))
            if res.status_code == 200:
                msg = 'کد گزاری تصاویر با موفیقت انجام شد'
            else:
                msg = 'خطا در اتصال به رزبری'
            ####### send api to encode image  ############################################################
        except Exception as e:
            print(str(e))
        return redirect('user_list')

    def post(self, request, *args, **kwargs):
        return redirect('user_list')


def get_user_list(request):
    search, page, per_page = get_datatable_query(request.GET)
    results, count = userprofile_model.objects.search(search, page=page, per_page=per_page)
    return JsonResponse(get_datatable_results(results, count, search), safe=False)


def delete_dataset_image(request, img_id):
    instance = userimage_model.objects.filter(id=int(img_id)).first()
    user_id = instance.user.id
    username = instance.user.user.username
    userimage_model.objects.filter(id=int(img_id)).delete()
    try:
        res = requests.post('http://localhost:8888/encoding', data=json.dumps(
            {'encoding': True, 'username': username, 'prof': 'Edited'}))
        if res.status_code == 200:
            msg = 'کد گزاری تصاویر با موفیقت انجام شد'
        else:
            msg = 'خطا در اتصال به رزبری'
    except Exception as e:
        print(str(e))

    return redirect('edit_user', user_id)

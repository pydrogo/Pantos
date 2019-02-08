from rest_framework.response import Response
from rest_framework.views import APIView
from frAdmin.apps.web.models import Camera as CameraModel
import requests


class ChangeCameraIP(APIView):
    def get(self, request, format=None):
        data = request.GET['data']
        camera = CameraModel.objects.get(username=data['change_camera_to_server']['previous_username'])
        if camera :
            camera.username=data['change_camera_to_server']['current_username']
            camera.password=data['change_camera_to_server']['current_password']
            camera.ip=data['change_camera_to_server']['current_ip']
            camera.save()
            return Response(data={'change_camera_to_server':{'result':True}})
        else:
            return Response(data={'change_camera_to_server':{'result':False}})
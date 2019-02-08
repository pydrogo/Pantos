from rest_framework.response import Response
from rest_framework.views import APIView
from frAdmin.settings import parameter


class ChangeRaspberry(APIView):
    def get(self, request, format=None):
        response = {'name': 'change_raspberry_ip', 'status': False}
        # try:
        #     previous_username = request.GET['previous_username']
        #     previous_password = request.GET['previous_password']
        #     previous_ip = request.GET['previous_password']
        #     new_username = request.GET['new_username']
        #     new_password = request.GET['new_password']
        #     new_ip = request.GET['new_ip']
        #     if (parameter.username == previous_username and parameter.password == previous_password and parameter.raspberry_ip == previous_ip):
        #         parameter.username = new_username
        #         parameter.password = new_password
        #         parameter.raspberry_ip = new_ip
        #         response['status']=True
        # except :
        #     pass
        return Response(response)

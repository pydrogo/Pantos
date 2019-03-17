import threading
import cv2
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators import gzip
from imutils.video import VideoStream
from frAdmin.apps.web.models.camera import Camera as CameraModel
import base64
#from frAdmin.apps.web.views.cam_module import cam

class VideoCamera(object):
    username = ''
    upass = ''
    ip = ''

    def __init__(self, username, upass, ip):
        self.video = cv2.VideoCapture(
            "rtsp://{0}:{1}@{2}:554/mode=real&idc=1&ids=3".format(username, upass, ip))
        (self.grabbed, self.frame) = self.video.read()
        print(str(self.grabbed))
        if self.grabbed:
            threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        resized_image = cv2.resize(image, (500, 350))
        ret, jpeg = cv2.imencode('.jpg', resized_image)
        return jpeg.tobytes()

    def get_snapshot(self):
        image = self.frame
        resized_image = cv2.resize(image, (500, 350))
        ret, jpeg = cv2.imencode('.jpg', resized_image)
        return base64.b64encode(jpeg.tobytes())

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


cam = None



def gen(username, upass, ip):
    
    global cam
    if cam is  None:
        cam = VideoCamera(username, upass, ip)
        
    print('before********')
    print(str(cam))
    
    print(str(cam))
    print('after********')
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_live_snapshot(username, upass, ip):
    global cam
    if cam is not None:
        return cam.get_snapshot()
    else:
        print('no active cam')
        cam = VideoCamera(username, upass, ip)
        return cam.get_snapshot()
    


@gzip.gzip_page
def stream(request):
    print('*********************************'+str(cam))
    try:
        cid = request.GET.get('cid', 0)
        camera = CameraModel.objects.filter(id=cid).first()
        if camera:
            username, upass, ip = camera.username, camera.password, camera.ip
        else:
            username, upass, ip = '', '', ''
        return StreamingHttpResponse(gen(username, upass, ip),
                                     content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass



@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


def get_snapshot(request):

    try:
        cid = request.GET.get('cid', 0)
        camera = CameraModel.objects.filter(id=cid).first()
        if camera:
            username, upass, ip = camera.username, camera.password, camera.ip
        else:
            username, upass, ip = '', '', ''
        # cam = VideoCamera()
        return HttpResponse(get_live_snapshot(username, upass, ip), content_type='image/jpeg')
    except:  # This is bad! replace it with proper handling
        return HttpResponse(None)


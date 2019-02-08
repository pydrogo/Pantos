import tornado.ioloop
import tornado.web


class AddCamera(tornado.web.RequestHandler):

    def get(self):
        res = {'status': True}
        self.write(res)

    def post(self):
        data = self.get_argument('data')
        camera_username = data['‫‪camera_username‬‬']
        camera_password = data['camera_password']
        camera_ip = data['camera_ip']
        camera_name = data['camera_name']

        # write your code about save new camera in raspberry
        # if you successfully save new camera return data = {'status':'success'}
        # else return data = {'status':'fail'}


class ChangeCamera(tornado.web.RequestHandler):

    def get(self):
        pass

    def post(self):
        data = self.get_argument('data')
        previous_username = data['previous_username']
        previous_password = data['previous_password']
        previous_ip = data['previous_ip']
        new_ip = data['new_ip']
        new_username = data['new_username']
        new_password = data['new_password']
        new_name = data['new_name']

        # write your code about change camera in raspberry with above information
        # if you successfully save change camera return data = {'status':'success'}
        # else return data = {'status':'fail'}


class ChangeRaspberry(tornado.web.RequestHandler):

    def get(self):
        pass

    def post(self):
        data = self.get_argument('data')
        previous_username = data['previous_username']
        previous_password = data['previous_password']
        previous_ip = data['previous_ip']

        new_username = data['new_username']
        new_password = data['new_password']
        new_ip = data['new_ip']
        dhcp = data['DHCP']  # true or false
        getway = data['getway']
        subnet_mask = data['subnet_mask']

        # write your code about change raspberry with above information (note that if dhcp is true you should use subnet_mask and getway)
        # if you successfully save change raspberry return data = {'status':'success'}
        # else return data = {'status':'fail'}


class Wifi(tornado.web.RequestHandler):

    def get(self):
        pass

    def post(self):
        data = self.get_argument('data')
        ssid = data['ssid']
        password = data['password']

        # write your code about set raspberry wifi with above information
        # if you successfully save wifi information return data = {'status':'success'}
        # else return data = {'status':'fail'}


application = tornado.web.Application([
    (r"/add_camera", AddCamera),
    (r"/change_camera", ChangeCamera),
    (r"/change_raspberry", ChangeRaspberry),
    (r"/wifi", Wifi),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


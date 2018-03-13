from camera import Camera


class CameraManager(object):
    def __init__(self):
        self.camera_list = []

    def get_cameras(self):
        return [item.id for item in self.camera_list]

    def add_camera(self, params):
        inst = Camera(camera_ip=params['ip'], auth=[params['user'], params['password']],
                      endpoint=params['endpoint'])

        self.camera_list.append(inst)
        inst.start()

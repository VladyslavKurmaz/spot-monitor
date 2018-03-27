import logging
from .camera import Camera

logger = logging.getLogger(__name__)


class CameraManager(object):
    def __init__(self):
        self.camera_list = []

    def get_camera(self, id):
        logger.debug("Get camera with identifier {}".format(id))
        for item in self.camera_list:
            if item.id == id:
                return {"id": item.id, "video_source": item.video_source, "endpoint": item.endpoint}
            else:
                return None

    def get_cameras(self):
        return [{"id": item.id, "video_source": item.video_source, "endpoint": item.endpoint}
                for item in self.camera_list]

    def add_camera(self, params):
        idn = int(params['ip'].split(':')[0].replace(".", ""))
        for item in self.camera_list:
            if item.id == idn:
                cam = self.get_camera(idn)
                logger.info("Camera instance already exists")
                return False, cam

        cam = Camera(idn=idn, camera_ip=params['ip'],
                     auth=[params['user'], params['password']],
                     endpoint=params['endpoint'])

        logger.info("Camera instance created")
        self.camera_list.append(cam)
        cam.start()
        logger.info("Camera instance started")

        cam = self.get_camera(idn)

        return True, cam

    def delete_camera(self, id):
        for idx, item in enumerate(self.camera_list):
            if item.id == id:
                obj = self.get_camera(id)
                self.camera_list[idx].stop()
                self.camera_list.pop(idx)
                logger.info("ID: [{}] Camera instance deleted".format(id))
                return True, obj
        logger.info("ID: [{}] No such camera instance".format(id))
        return False, {}


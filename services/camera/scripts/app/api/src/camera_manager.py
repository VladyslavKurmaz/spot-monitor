import logging
from .camera import Camera

logger = logging.getLogger(__name__)


class CameraManager(object):
    def __init__(self):
        self.object_counter = 0
        self.camera_list = []

    def get_stream(self, id):
        for item in self.camera_list:
            if item.id == id:
                return item.get_frame

    def get_camera(self, id):
        logger.debug("Get camera with identifier {}".format(id))
        for item in self.camera_list:
            if item.id == id:
                return {"id": item.id, "video_source": item.video_source,
                        "endpoint": item.endpoint, 'health': not item.stopped,
                        "stream_url": item.stream_url}
            else:
                return None

    def get_cameras(self):
        return [{"id": item.id, "video_source": item.video_source, "endpoint": item.endpoint,
                 'health': not item.stopped, "stream_url": item.stream_url}
                for item in self.camera_list]

    def add_camera(self, params):
        self.object_counter += 1
        for item in self.camera_list:
            if item.video_source == params['ip']:
                cam = self.get_camera(item.id)
                logger.info("Camera instance already exists")
                return False, cam

        cam = Camera(idn=self.object_counter, camera_ip=params['ip'],
                     auth=[params['user'], params['password']],
                     endpoint=params['endpoint'])

        logger.info("Camera instance created")
        self.camera_list.append(cam)
        cam.start()
        logger.info("Camera instance started")

        cam = self.get_camera(self.object_counter)

        return True, cam

    def delete_camera(self, id):
        for idx, item in enumerate(self.camera_list):
            if item.id == id:
                obj = self.get_camera(id)
                self.camera_list[idx].stop()
                self.camera_list[idx].join()
                self.camera_list.pop(idx)
                logger.info("Camera instance ID=[{}] deleted".format(id))
                return True, obj
        logger.info("No such camera ID=[{}] instance".format(id))
        return False, {}


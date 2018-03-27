import logging
from threading import Thread

import time
import json

import requests
import cv2

logger = logging.getLogger(__name__)


class Camera(Thread):
    def __init__(self, idn, camera_ip, auth, endpoint):
        super(Camera, self).__init__()
        self.stopped = False
        self.error_counter = 0

        self.id = idn
        self.log = "[{}] ".format(self.id)

        self.video_source = camera_ip
        self.device_url = "rtsp://{}:{}@{}/Streaming/Channels/101".format(auth[0], auth[1], camera_ip)
        self.cam = cv2.VideoCapture(self.device_url)
        self.endpoint = endpoint

    def _run(self):
        """
            _run function for compatibility with greenlet
        """
        self.run()

    def run(self):
        """
            run function for compatibility with thread
        """
        while not self.stopped:

            if self.error_counter > 50:
                logger.error(self.log + "Error counter exceeded: {}".format(self.error_counter))
                break

            ret, frame = self.cam.read()

            if not ret:
                logger.warning(self.log + "Couldn't obtain frame, error counter {}".format(self.error_counter))
                self.error_counter += 1
                time.sleep(1)
                continue

            _, img_encoded = cv2.imencode('.jpg', frame)
            files = {
                "img": ("img", img_encoded.tostring(), "image/jpeg"),
                "json": ("jf", json.dumps({"cam_id": self.id}), 'application/json'),
            }
            try:
                response = requests.post(self.endpoint, files=files)
                logger.debug(self.log + "Responce code: {}".format(response.status_code))
            except Exception as e:
                logger.error(self.log + "Consuming service error: {}".format(e))
                self.error_counter += 1
                time.sleep(1)

        self.release()

    def stop(self):
        self.stopped = True

    def release(self):
        self.cam.release()
        logger.info(self.log + "Camera released")

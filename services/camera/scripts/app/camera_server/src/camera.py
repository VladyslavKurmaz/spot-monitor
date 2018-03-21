import logging
from threading import Thread

import time
import json

import requests
import cv2

logger = logging.getLogger('gunicorn.error')


class Camera(Thread):
    def __init__(self, camera_ip, auth, endpoint):
        super(Camera, self).__init__()
        self.stopped = False
        self.id = camera_ip

        self.device_url = "rtsp://{}:{}@{}/Streaming/Channels/101".format(auth[0], auth[1], camera_ip)
        self.cam = cv2.VideoCapture(self.device_url)

        self.endpoint = endpoint

        self.error_counter = 0

    def run(self):

        while not self.stopped:

            if self.error_counter > 50:
                logger.debug("[CAMERA] [{}] Error counter exceeded".format(self.id))
                break

            ret, frame = self.cam.read()

            if not ret:
                logger.debug("[CAMERA] [{}] Couldn't obtain frame".format(self.id))
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
                logger.debug("[CAMERA] [{}] {}".format(self.id, response))
            except Exception as e:
                logger.debug("[CAMERA] [{}] Consuming service error: {}".format(self.id, e))
                self.error_counter += 1
                time.sleep(1)

        self.release()

    def stop(self):
        self.stopped = True

    def release(self):
        self.cam.release()
        logger.debug("[CAMERA] [{}] Released".format(self.id))

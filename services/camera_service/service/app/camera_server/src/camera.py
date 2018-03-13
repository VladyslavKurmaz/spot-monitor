from multiprocessing import Process

import requests
import cv2


class Camera(Process):
    def __init__(self, camera_ip, auth, endpoint):
        super(Camera, self).__init__()
        self.stopped = False
        self.id = camera_ip

        self.device_url = "rtsp://{}:{}@{}/Streaming/Channels/101".format(auth[0], auth[1], camera_ip)
        self.cam = cv2.VideoCapture(self.device_url)

        self.endpoint = endpoint

        self.headers = {'content-type': 'image/jpeg'}
        self.no_frame_counter = 0

    def run(self):
        while not self.stopped:
            ret, frame = self.cam.read()

            if ret:
                if self.no_frame_counter > 50:
                    print("No camera connection")
                    break
                else:
                    self.no_frame_counter += 1

            _, img_encoded = cv2.imencode('.jpg', frame)
            response = requests.post(self.endpoint, data=img_encoded.tostring(), headers=self.headers)
            print(response)

        self.release()

    def stop(self):
        self.stopped = True

    def release(self):
        self.cam.release()

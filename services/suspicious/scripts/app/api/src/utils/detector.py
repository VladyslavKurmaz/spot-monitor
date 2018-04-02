import os
import json
import logging

import requests
import numpy as np

logger = logging.getLogger(__name__)


class Detector:
    def __init__(self):
        # self.endpoint = "http://" + os.environ['AWS_GPU_IP'] + ":8000/detect"
        self.endpoint = "http://192.168.3.169:8002/detect"
        self.headers = {'content-type': 'image/jpeg'}
        logger.debug("[DETECTOR] Endpoint: {}".format(self.endpoint))

    def detect(self, im):
        response = requests.post(self.endpoint, data=im, headers=self.headers)
        res = json.loads(response.text)
        logger.debug("[DETECTOR] Responce from Detector {}".format(res))

        centers = []
        contours = []

        for key in res:
            for items in res[key]:
                x = items[0] + items[2] / 2
                y = items[3] + items[1] / 2
                centers.append(np.array([x, y], dtype=np.int32))
                contours.append(np.array([
                    [[items[0], items[1]]],
                    [[items[2], items[1]]],
                    [[items[2], items[3]]],
                    [[items[0], items[3]]]
                ], dtype=np.int32))

        return centers, contours





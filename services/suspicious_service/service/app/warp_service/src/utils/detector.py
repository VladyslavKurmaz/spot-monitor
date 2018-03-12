import json
import requests


class Detector:
    def __init__(self):
        self.endpoint = '' # let say here we have some endpoint
        self.headers = {'content-type': 'image/jpeg'}

    def detect(self, im):
        response = requests.post(self.endpoint, data=im.tostring(), headers=headers)
        # TODO: parse response
        res = json.loads(response.text)

        centers = []
        contours = []

        for key in res:
            for items in res[key]:
                x = items[0] + items[2] / 2
                y = items[3] + items[1] / 2
                centers.append([x, y])
                contours.append([[items[0], items[1]],
                                 [items[2], items[1]],
                                 [items[0], items[3]],
                                 [items[2], items[3]]])
        return centers, contours





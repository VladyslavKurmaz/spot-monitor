import os

import yaml
import numpy as np

import cv2
from skimage import transform as tf


cur_path = os.path.abspath(os.path.dirname(__file__))
conf_path = os.path.join(cur_path, 'warper', 'conf.yaml')


class Warper:
    def __init__(self):
        with open(conf_path, 'r') as f:
            self.conf = yaml.load(''.join(f.readlines()))

        self.shape = self.conf['map']['size']

    def get_markers(self, key):
        if key == 'map':
            return np.array(self.conf[key]['markers'])
        else:
            for i in self.conf['cameras']:
                if i['id'] == key:
                    return np.array(i['markers'])

    def warp_image(self, img_shape, coordinates, camera_id):
        if len(coordinates) == 0:
            return []

        transform = tf.ProjectiveTransform

        mask = np.zeros((img_shape[0], img_shape[1], 1), dtype=np.uint8)
        cv2.fillPoly(mask, pts=coordinates, color=(255, 255, 255))

        tform3 = transform()
        tform3.estimate(self.get_markers('map'), self.get_markers(camera_id))

        warped_mask = tf.warp(mask, tform3, output_shape=self.shape) * 255
        ret, thresh = cv2.threshold(warped_mask.astype(np.uint8), 127, 255, cv2.THRESH_BINARY)

        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours

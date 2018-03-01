import os
import cv2
import numpy as np

cur_path = os.path.abspath(os.path.dirname(__file__))

class SimpleDetector(object):
    """
        Detector class
    """

    def __init__(self, logger):
        """
        Detector initializer
        """
        self.name = "SimpleDetector"
        self.logger = logger
        self.kernel = (13, 13)
        self.base_frame = cv2.imread(os.path.join(cur_path, "capture.jpg"),
                                     cv2.IMREAD_GRAYSCALE | cv2.IMREAD_IGNORE_ORIENTATION)
        self.base_frame = cv2.GaussianBlur(self.base_frame, self.kernel, 0)

        self.filtered_centers = None
        self.cntrs = None

    def detect(self, im):
        """
        Detect regions on image
        Detection algorithm based on simple subtraction of current and reference frame
        :param im: image
        :return: centers of regions (filtered with simple heuristic)
        """
        result = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        result = cv2.GaussianBlur(result, self.kernel, 0)
        result = cv2.absdiff(result, self.base_frame)
        result = cv2.threshold(result, 50, 255, cv2.THRESH_BINARY)[1]
        result = cv2.dilate(result, None, iterations=2)

        cntrs = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

        self.filtered_centers = []
        self.cntrs = []

        for it, cnt in enumerate(cntrs):

            area = cv2.contourArea(cnt)
            self.logger.debug("{0} {1}".format(self.name, "Contour instance {0} area: {1}".format(it, area)))
            if area < 10000:
                self.logger.debug("{0} {1}".format(self.name, "Contour instance {0} too small".format(it)))
                continue

            self.cntrs.append(cnt)

            # find center
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            self.filtered_centers.append(np.array([cx, cy]))

        return self.filtered_centers, self.cntrs
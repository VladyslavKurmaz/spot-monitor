from threading import Lock
import logging

import numpy as np
import cv2

from utils.detector import Detector
from utils.tracking import Tracker
from utils.warper import Warper

logger = logging.getLogger('gunicorn.error')


class SpotMonitor:
    def __init__(self, cam_id):
        self.id = cam_id

        self.lock = Lock()

        self.detector = Detector()
        self.tracker = Tracker(skipped_th=5)
        self.warper = Warper()

        self.suspicious_regions = None

    def process(self, im):
        with self.lock:
            filtered_centers, cntrs = self.detector.detect(im=im)
            logger.debug("[SPOT MONITOR] [{}] Centers: {} Contours: {}".
                          format(self.id, filtered_centers, cntrs))

            nparr = np.frombuffer(im, np.uint8)
            im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            tracks, susp_reg = self.tracker.track(centers=filtered_centers, cntrs=cntrs)

            logger.debug("[SPOT MONITOR] [{}] Suspicious region: {} ".
                          format(self.id, susp_reg))

            bbox_warped = self.warper.warp_image(img_shape=[im.shape[0], im.shape[1]],
                                                 coordinates=susp_reg, camera_id=1)

            logger.debug("[SPOT MONITOR] [{}] Warped suspicious region: {} ".
                          format(self.id, bbox_warped))

            susp_reg = [i.tolist() for i in susp_reg]
            bbox_warped = [i.tolist() for i in bbox_warped]

            self.suspicious_regions = {'suspicious': susp_reg, "mapped": bbox_warped}







from threading import Lock

from utils.detector import Detector
from utils.tracking import Tracker
from utils.warper import Warper


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
            tracks, susp_reg = self.tracker.track(centers=filtered_centers, cntrs=cntrs)
            bbox_warped = self.warper.warp_image(img_shape=[im.shape[0], im.shape[1]],
                                                 coordinates=susp_reg, camera_id=1)
            self.suspicious_regions = {'suspicious': susp_reg, "mapped": bbox_warped}







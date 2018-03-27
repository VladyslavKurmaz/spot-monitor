import logging
from spotmonitor import SpotMonitor

logger = logging.getLogger(__name__)


class SpotManager:
    def __init__(self):
        self.monitors = {}

    def get_region(self, idf):
        logger.debug("get_region request with identifier {}".format(idf))
        if idf in self.monitors.keys():
            return True, self.monitors[idf].suspicious_regions
        else:
            return False, {}

    def get_all(self):
        return [{idx: self.monitors[idx].suspicious_regions} for idx in self.monitors]

    def create_monitor(self, idf):
        logger.debug("create_monitor request with identifier {}".format(idf))
        if idf in self.monitors.keys():
            return False
        else:
            self.monitors[idf] = SpotMonitor(cam_id=idf)
            return True

    def process_monitor(self, idf, img):
        logger.debug("process_monitor request with identifier {}".format(idf))
        if idf in self.monitors.keys():
            self.monitors[idf].process(img)
            return True, self.monitors[idf].suspicious_regions
        else:
            return False, {}
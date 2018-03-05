import logging
import logging.config

import os

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from threading import Thread
from Queue import Queue, Empty

import cv2

from detectors.simple_detector import SimpleDetector
from utils.tracking import Tracker
from utils.warper import Warper


class SpotMonitor(Thread):
    def __init__(self, q_image, q_result):
        super(SpotMonitor, self).__init__()
        self.stopped = False
        self.q_image = q_image
        self.q_result = q_result

        self.detector = SimpleDetector(logger)
        self.tracker = Tracker(skipped_th=5)
        self.warper = Warper()

    def run(self):
        while True:
            try:
                frm = self.q_image.get(False, 1)
                im = frm.copy()

                filtered_centers, cntrs = self.detector.detect(im=im)
                tracks, susp_reg = self.tracker.track(centers=filtered_centers, cntrs=cntrs)
                bbox_warped = self.warper.warp_image(img=im, coordinates=susp_reg, camera_id=1)

                cv2.drawContours(im, susp_reg, -1, (0, 255, 0), 5)

                for item in tracks:
                    trace = item.trace

                    for points in trace:
                        cv2.circle(im, (int(points[0]), int(points[1])), 3, (255, 0, 0), -1)

                    cv2.putText(im, "Track {0}".format(item.trackID), (int(trace[-1][0]), int(trace[-1][1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)

                self.q_image.task_done()
                self.q_result.put([im, bbox_warped])

            except Empty:
                if self.stopped:
                    return
            except:
                raise

    def stop(self):
        self.stopped = True


if __name__ == "__main__":

    cam = cv2.VideoCapture("rtsp://admin:admin123@172.22.61.80:554/Streaming/Channels/101")
    deck_map = cv2.imread(os.path.join(".", "conf", "warper", "td_map.jpg"))

    q_image = Queue()
    q_result = Queue()

    sp = SpotMonitor(q_image, q_result)

    sp.start()
    counter = 0
    while True:
        if counter > 10:
            break

        ret, frame = cam.read()
        if ret:
            q_image.put(frame)
        else:
            counter += 1
            continue

        frame, susp_region = q_result.get()

        q_result.task_done()
        cv2.imshow("Result", frame)

        im = deck_map.copy()

        cv2.drawContours(im, susp_region, -1, (0, 255, 0), 5)
        cv2.imshow("Map", im)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    sp.stop()

    q_image.join()
    q_result.join()

    sp.join()

    cam.release()
    cv2.destroyAllWindows()

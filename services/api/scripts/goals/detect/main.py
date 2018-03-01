import logging
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from threading import Thread
from Queue import Queue, Empty

import numpy as np
import cv2

from detectors.simple_detector import SimpleDetector
from utils.tracking import Tracker


class SpotMonitor(Thread):
    def __init__(self, q_image, q_result):
        super(SpotMonitor, self).__init__()
        self.stopped = False
        self.q_image = q_image
        self.q_result = q_result

        self.detector = SimpleDetector(logger)
        self.tracker = Tracker(skipped_th=5)

    def run(self):
        while True:
            try:
                im = self.q_image.get(False, 1)

                filtered_centers, cntrs = self.detector.detect(im=im)
                tracks = self.tracker.track(centers=filtered_centers)

                for item in tracks:
                    trace = item.trace
                    if len(trace) > 10:
                        dist = np.sqrt((trace[-1][0] - trace[-2][0]) ** 2 + (trace[-1][1] - trace[-2][1]) ** 2)
                        if dist < 5:
                            item.too_long += 1
                        else:
                            item.too_long = 0

                    for points in trace:
                        if item.too_long > 5:
                            cv2.circle(im, (int(points[0]), int(points[1])), 3, (0, 0, 255), -1)
                        else:
                            cv2.circle(im, (int(points[0]), int(points[1])), 3, (255, 0, 0), -1)

                    cv2.putText(im, "Track {0}".format(item.trackID), (int(trace[-1][0]), int(trace[-1][1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)

                self.q_image.task_done()
                self.q_result.put(im)

            except Empty:
                if self.stopped:
                    return
            except:
                raise

    def stop(self):
        self.stopped = True


if __name__ == "__main__":

    cam = cv2.VideoCapture("rtsp://admin:admin123@172.22.61.80:554/Streaming/Channels/101")

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

        frame = q_result.get()
        q_result.task_done()
        cv2.imshow("Result", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    sp.stop()

    q_image.join()
    q_result.join()

    sp.join()
    
    cam.release()
    cv2.destroyAllWindows()
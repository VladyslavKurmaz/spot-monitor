import logging

from threading import Thread, Event

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident

import time

import requests
import cv2

logger = logging.getLogger(__name__)


def stream(idf, username, password, video_source):
    """
        Generator that returns stream from camera
    :return:
    """
    log = "[STREAM] [{}] ".format(idf)
    stream_src = "rtsp://{}:{}@{}/Streaming/Channels/101".format(username, password, video_source)
    frame_absence_counter = 0
    try:
        cam = cv2.VideoCapture(stream_src)
        logger.debug(log + "VideoCapture Ok")
    except Exception as e:
        logger.error(log + "cv2.VideoCapture encountered an error: {}".format(e))
        raise IOError("Couldn't open resource")

    while True:
        ret, frame = cam.read()
        if frame_absence_counter > 50:
            logger.error(log + "Error counter exceeded: {}".format(frame_absence_counter))
            cam.release()
            raise RuntimeError(log + "Error counter exceeded: {}".format(frame_absence_counter))

        if not ret:
            logger.warning(log + "Couldn't obtain frame, error counter {}".format(frame_absence_counter))
            frame_absence_counter += 1
            time.sleep(1)
            continue

        else:
            yield cv2.imencode('.jpg', frame)[1].tostring()


class CameraEvent:
    """
        Event-like class for signaling all clients that frame is available
    """
    def __init__(self):
        self.log = "[CAMERA EVENT] "
        self.events = {}

    def wait(self):
        ident = get_ident()
        logging.debug(self.log + "wait() ident: {} Enter function".format(ident))
        if ident not in self.events:
            self.events[ident] = Event()
            logging.debug(self.log + "wait() ident: {} Create event".format(ident))

        return self.events[ident].wait()

    def set(self):
        for ident in self.events:
            if not self.events[ident].isSet():
                self.events[ident].set()
                logging.debug(self.log + "set() ident: {} Event set".format(ident))

    def clear(self):
        ident = get_ident()
        self.events[ident].clear()
        logging.debug(self.log + "set() ident: {} Clear event".format(ident))


class Camera(Thread):
    def __init__(self, idn, camera_ip, auth, endpoint):
        super(Camera, self).__init__()
        self.stopped = False
        self.error_counter = 0

        self.id = idn
        self.log = "[{}] ".format(self.id)

        self.video_source = camera_ip
        self.username = auth[0]
        self.password = auth[1]
        self.dst_url = endpoint
        self.endpoint = None

        self.event = CameraEvent()
        self.frame = None

        self.stream = Thread(target=self._thread)
        self.stream.start()

        self.configure()

    def configure(self):
        """
        This method creates resource on suspicious server, that will obtain img data from camera
        :return:
        """
        try:
            response = requests.post(self.dst_url, json={"cam_id": self.id})
            logger.debug(self.log + "Response code: {}".format(response.status_code))

            while self.get_frame() is None:
                time.sleep(0)

            logger.debug(self.log + "Configured")
        except Exception as e:
            logger.error(self.log + "Unable to create resource: {}".format(e))
            # self.stop()

    def _thread(self):
        """
        Camera background thread
        """
        logger.debug(self.log + "Starting background camera stream")
        frames_iterator = stream(self.id, self.username, self.password, self.video_source)
        im = None

        while True:
            try:
                im = next(frames_iterator)
            except Exception as e:
                logging.error(self.log + "Error in background thread: {}".format(e))
                self.stop()

                if self.stopped:
                    frames_iterator.close()
                    return

            self.frame = im
            self.event.set()
            time.sleep(0)

    def get_frame(self):
        self.event.wait()
        self.event.clear()

        return self.frame

    def _run(self):
        """
            _run function for compatibility with greenlet
        """
        self.run()

    def run(self):
        """
            run function for compatibility with thread
        """

        while not self.stopped:

            if self.error_counter > 50:
                logger.error(self.log + "Error counter exceeded: {}".format(self.error_counter))
                self.stop()

            img = self.get_frame()

            try:
                response = requests.post(self.endpoint, data=img, headers={'content-type': 'image/jpeg'})
                logger.debug(self.log + "Response code: {}".format(response.status_code))
            except Exception as e:
                logger.error(self.log + "Consuming service error: {}".format(e))
                logger.error(self.log + "Error counter: {}".format(self.error_counter))
                self.error_counter += 1
                time.sleep(1)

    def stop(self):
        self.stopped = True
        logger.debug(self.log + "Service stopped")

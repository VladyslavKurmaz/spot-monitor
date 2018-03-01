import cv2
import logging
import numpy as np


from utils.kalman_filter import KalmanFilter
from scipy.optimize import linear_sum_assignment


class Track(object):
    """
        Class that describe track
    """
    def __init__(self, trackID, initial_state_vector):
        """
        Track initialization
        :param trackID: track identifier
        :param initial_state_vector: region's center coordinates when it's firstly appeared
        """
        self.trackID = trackID
        self.kf = KalmanFilter(x=initial_state_vector)
        self.trace = [initial_state_vector]
        self.skipped_frames = 0
        self.too_long = 0


class Tracker(object):
    """
        Class that perform region tracking
    """
    def __init__(self, dist_th=100, skipped_th=50):
        """
        Initialization
        :param dist_th: Distance threshold between predicted and real position of region center,
                        need for Hungarian algo
        :param skipped_th: Number of frames count from last appearance of track before delete it
        """
        self.tracks = []
        self.trackIDCounter = 0
        self.dist_threshold = dist_th
        self.nb_skipped_frames_threshold = skipped_th

    def track(self, centers):
        """
        Perform basic tracking.
        Predict next position with Kalman filter, assign real regions centers to predicted centers with
        Hungarian algorithm, and add simple track management
        :param centers:
        :return: tracks
        """

        """
            Initialization
            1) Create first tracks for first regions
            2) Init Kalman filter of each track with centers of detected regions
        """

        if len(self.tracks) == 0:
            for it in centers:
                self.tracks.append(Track(self.trackIDCounter, it))
                self.trackIDCounter += 1

        """
            Assign tracks with detections
            1) Compute euclidean distance between track and centers
            2) Solve assignment problem with Hungarian algorithm 
        """

        nb_tracks = len(self.tracks)
        nb_centers = len(centers)

        cost_matrix = np.zeros(shape=(nb_tracks, nb_centers))

        for i in range(len(self.tracks)):
            for j in range(len(centers)):
                distance_square = np.power(self.tracks[i].trace[-1][0] - centers[j][0], 2) + \
                                  np.power(self.tracks[i].trace[-1][1] - centers[j][1], 2)
                distance = np.sqrt(distance_square)
                cost_matrix[i][j] = distance

        assignment = [-1] * nb_tracks
        row_idx, col_idx = linear_sum_assignment(cost_matrix)

        for i in range(len(row_idx)):
            assignment[row_idx[i]] = col_idx[i]

        """
            Track and detection management
            1) Manage tracks that to far from centroid
            2) Identify tracks with no assignment
            3) Delete track that were not detected for a long time
            4) Identify detection without tracks and create ones
        """
        for i in range(len(assignment)):
            if assignment[i] == -1:
                self.tracks[i].skipped_frames += 1
            else:
                if cost_matrix[i][assignment[i]] > self.dist_threshold:
                    assignment[i] = -1
                    self.tracks[i].skipped_frames += 1

        del_tracks = []

        for i in range(len(self.tracks)):
            if self.tracks[i].skipped_frames > self.nb_skipped_frames_threshold:
                del_tracks.append(i)

        if len(del_tracks):
            for i in del_tracks:
                del self.tracks[i]
                del assignment[i]

        un_assigned_detection = []

        for i in range(len(centers)):
            if i not in assignment:
                un_assigned_detection.append(i)

        if len(un_assigned_detection):
            for i in un_assigned_detection:
                self.tracks.append(Track(self.trackIDCounter, centers[i]))
                self.trackIDCounter += 1

        """
            Prediction with Kalman filter
            1) Predict new positions of centers of objects and save them in a history
        """
        for i in range(len(assignment)):
            if assignment[i] != -1:
                self.tracks[i].skipped_tracks = 0
                self.tracks[i].trace.append(
                    self.tracks[i].kf.update(
                        centers[assignment[i]]
                    )[0]
                )
            else:
                self.tracks[i].trace.append(
                    self.tracks[i].kf.update(
                        self.tracks[i].trace[-1]
                    )[0]
                )

        return self.tracks


if __name__ == "__main__":
    import pickle
    # logger configuration
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    name = "[{0}]".format("Tracking")

    detector = SimpleDetector()
    tracker = Tracker(skipped_th=5)

    cam = cv2.VideoCapture("rtsp://admin:admin123@172.22.61.80:554/Streaming/Channels/101")

    archive = []
    # cam = cv2.VideoCapture(0)

    while True:
        _, frame = cam.read()

        logger.debug("{0} {1}". format(name, frame.shape))

        filtered_centers, cntrs = detector.detect(im=frame)

        # Draw centers and contours
        for centr, contour in zip(filtered_centers, cntrs):
            cv2.circle(frame, (centr[0], centr[1]), 3, (255, 0, 0), -1)
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        tracks = tracker.track(centers=filtered_centers)

        for item in tracks:
            trace = item.trace
            if len(trace) > 10:
                # logger.info("{0} {1}".format(name, "Len trace: {0}".format(len(trace))))
                if len(archive) == 0:
                    archive.append(item)
                    # logger.info("{0} {1}".format(name, "TrackID: {0}".format(item.trackID)))
                else:
                    arc_ids = [it.trackID for it in archive]
                    if item.trackID in arc_ids:
                        same_elem_idx = arc_ids.index(item.trackID)
                        if len(archive[same_elem_idx].trace) < len(trace):
                            archive[same_elem_idx] = item
                        logger.info("{0} {1}".format(name, "TrackID archived: {0}, trace len: {1}".format(item.trackID,
                                                                                                          len(trace))))
                    else:
                        # logger.info("/////////////////////////////////////////////////////")
                        # logger.info("{0} {1}".format(name, "TrackID returned: {0}".format(item.trackID)))
                        # logger.info("{0} {1}".format(name, "Len trace: {0}".format(len(trace))))
                        # logger.info("/////////////////////////////////////////////////////")
                        archive.append(item)

        # logger.info("{0} {1}".format(name, "Number of archived tracks: {0}".format(len(archive))))
        if len(archive) > 15:
            f = open("tracks.pkl", "wb")
            pickle.dump(archive, f)
            break

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
                    cv2.circle(frame, (int(points[0]), int(points[1])), 3, (0, 0, 255), -1)
                else:
                    cv2.circle(frame, (int(points[0]), int(points[1])), 3, (255, 0, 0), -1)

            cv2.putText(frame, "Track {0}".format(item.trackID), (int(trace[-1][0]), int(trace[-1][1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)

        logger.debug("{0} {1}".format(name, "Number of tracks: {}".format(len(tracks))))

        cv2.imshow("Original", frame)
        # cv2.imshow("Diff", result)
        # cv2.imshow("Base", base_frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


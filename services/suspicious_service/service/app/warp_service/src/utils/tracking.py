import cv2
import logging
import numpy as np


from kalman_filter import KalmanFilter
from scipy.optimize import linear_sum_assignment


class Track(object):
    """
        Class that describe track
    """
    def __init__(self, trackID, initial_state_vector, cntr):
        """
        Track initialization
        :param trackID: track identifier
        :param initial_state_vector: region's center coordinates when it's firstly appeared
        """
        self.trackID = trackID
        self.kf = KalmanFilter(x=initial_state_vector)
        self.trace = [initial_state_vector]
        self.contour = cntr
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

    def track(self, centers, cntrs):
        """
        Perform basic tracking.
        Predict next position with Kalman filter, assign real regions centers to predicted centers with
        Hungarian algorithm, and add simple track management
        :param centers:
        :param cntrs: contours
        :return: tracks
        """

        """
            Initialization
            1) Create first tracks for first regions
            2) Init Kalman filter of each track with centers of detected regions
        """

        if len(self.tracks) == 0:
            for center, cntr in zip(centers, cntrs):
                self.tracks.append(Track(self.trackIDCounter, center, cntr))
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

        if len(del_tracks) > 0:
            for i in reversed(del_tracks):
                del self.tracks[i]
                del assignment[i]

        un_assigned_detection = []

        for i in range(len(centers)):
            if i not in assignment:
                un_assigned_detection.append(i)

        if len(un_assigned_detection):
            for i in un_assigned_detection:
                self.tracks.append(Track(self.trackIDCounter, centers[i], cntrs[i]))
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
                self.tracks[i].contour = cntrs[assignment[i]]

        suspicious_regions = []

        for item in self.tracks:
            trc = item.trace
            if len(trc) > 5:
                dist = np.sqrt((trc[-1][0] - trc[-2][0]) ** 2 + (trc[-1][1] - trc[-2][1]) ** 2)
                if dist < 5:
                    item.too_long += 1
                else:
                    item.too_long = 0

            if item.too_long > 5:
                suspicious_regions.append(item.contour)

        return self.tracks, suspicious_regions
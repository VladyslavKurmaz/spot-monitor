from __future__ import print_function
import numpy as np


class KalmanFilter(object):
    """
        Kalman Filter class keeps track of the estimated state of
        the system and the variance or uncertainty of the estimate.
        Predict and Correct methods implement the functionality

        Reference:  https://en.wikipedia.org/wiki/Kalman_filter
                    http://nbviewer.jupyter.org/github/balzer82/Kalman/blob/master/Kalman-Filter-Step.png
    """

    def __init__(self, x):
        """
            Initialize variable used by Kalman Filter class

        """
        self.dt = 0.0  # delta time
        """
            H is the observation model which maps the true state space into the observed space
        """
        self.H = np.array([[1, 0], [0, 1]])
        """
            x is the state vector (for example a vector of coordinates of tracking object's center)
        """
        self.x = x  # previous state vector shape (2, 1)
        """
            P stands for variance-covariance matrix
        """
        self.P = np.diag((10., 10.))  # covariance matrix
        """
            F stands for state transition matrix 
        """
        self.F = np.array([[1.0, self.dt], [0.0, 1.0]])  # state transition mat
        """
            Q stands for noise covariance matrix
        """
        self.Q = np.eye(self.x.shape[0])  # process noise matrix
        """
            R stands for measurement error (sensor noise covariance matrix)
        """
        self.R = np.eye(self.x.shape[0])  # observation noise matrix

        self.history = list()

    def predict(self):
        """
            Predict state vector x and variance of uncertainty P (covariance).
        """
        """
            Predict current state vector x
            x_{k|p} = Fx_{k-1}
        """
        self.x = np.round(np.dot(self.F, self.x))
        """
            P_{k|p} = FP_{k-1}F.T + Q
        """
        self.P = np.dot(self.F, np.dot(self.P, self.F.T)) + self.Q

    def correct(self, z):
        """
            Correct or update state vector u and variance of uncertainty P (covariance).
        Args:
            z: vector of observations
        Return:
            predicted state vector x and P
        """

        """
            Computer kalman gain
            K_{k} = P_{k} H.T C.INV
            C = H P_{k} H.T + R
            
        """
        C = self.H.dot(np.dot(self.P, self.H.T)) + self.R
        K = np.dot(self.P.dot(self.H.T), np.linalg.inv(C))

        """
            Update estimation via measurement
            x_{k} = x_{k} + K_{k}(z_{k} - Hx_{k})
        """

        self.x = np.round(self.x + K.dot(z - np.dot(self.H, self.x))) # np.round because pixel can't be partial

        """
            Update covariance matrix
            P_{k} = (I - K_{k}H)P_{k|p}
            
            P_{k|p} - predicted covariance matrix
            
        """

        self.P = self.P - np.dot(np.dot(K, self.H), self.P)

        self.history.append([self.x, self.P])
        # TODO: Don't forget to delete this
        self.history = self.history[:10]

        return self.x, self.P

    def update(self, observation):
        self.predict()
        return self.correct(z=observation)


if __name__ == "__main__":
    kf = KalmanFilter(x=np.array([[10], [10]]))
    a = kf.update(observation=np.array([[10], [10]]))
    observation = np.array([[[11], [10]], [[13], [12]], [[15], [13]], [[20], [17]], [[25], [20]]])
    for i in range(observation.shape[0]):
        pos, cov = kf.update(observation[i])
        print("r_x = {0} r_y = {1}".format(observation[i][0][0], observation[i][1][0]))
        print("k_x = {0} k_y = {1}".format(pos[0][0], pos[1][0]))
        print("cov_x = {0} cov_y = {1}".format(cov[0][0], cov[1][1]))
        print("________________________________________________________________________")


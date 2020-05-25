import numpy as np
import random


# initial pose is [x, y, x', y'] T
# measure variance is variance in measurements over [x, y, x', y']
# acceleration variance is how much acceleration is expected to change the system
# controls are 0
class KalmanFilter:
    def __init__(self, initial_pose, initial_time, initial_covariance=1, accel_variance=30, measure_variance=1):
        self.pose = initial_pose
        self.time = initial_time
        self.covariance = initial_covariance * np.eye(4)
        self.accel_variance = accel_variance
        # Measurement is pose
        self.measure_matrix = np.eye(4)
        self.measurement_uncertainty = measure_variance * np.eye(4)
        self.I = np.eye(4)

    # Predict new position and error (covariance)
    def predict(self, to_time):
        # Predict new pose
        dt = to_time - self.time
        A = np.eye(4)
        A[0, 2] = dt
        A[1, 3] = dt
        new_pose = np.dot(A, self.pose)
        # Update covariance
        new_covariance = np.dot(np.dot(A, self.covariance), np.transpose(A)) + self.noise_covariance(to_time)
        return new_pose, new_covariance

    # Assuming acceleration variance is equal in x, y direction
    # This matrix takes into account how far off our guess might be, if acceleration changes velocity
    def noise_covariance(self, to_time):
        dt = to_time - self.time
        G = np.transpose(np.asarray([[0.5 * dt ** 2, 0.5 * dt ** 2, dt, dt]]))
        Q = np.dot(np.dot(G, np.transpose(G)), self.accel_variance)
        return Q

    # Update the estimated position and covariance with new information about pose
    def update(self, new_pose, est_pose, est_covariance):
        # Correction step
        measurement_residual = new_pose - np.dot(self.measure_matrix, est_pose)
        S = np.linalg.inv(self.measurement_uncertainty + np.dot(np.dot(self.measure_matrix, est_covariance),
                np.transpose(self.measure_matrix)))
        kalman_gain = np.dot(np.dot(est_covariance,  np.transpose(self.measure_matrix)), S)
        corrected_pose = new_pose + np.dot(kalman_gain, measurement_residual)
        corrected_covariance = np.dot((self.I - np.dot(kalman_gain, self.measure_matrix)), est_covariance)
        return corrected_pose, corrected_covariance

    # Update given [time, x, y, x', y']
    def update_simple(self, new_pose, new_time):
        est_pose, est_covariance = self.predict(new_time)
        self.pose, self.covariance = self.update(new_pose, est_pose, est_covariance)
        self.time = new_time


if __name__ == "__main__":
    print("Hi")

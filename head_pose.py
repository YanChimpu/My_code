#!/usr/bin/env python

import cv2
import numpy as np
from landmarks import LandmarksDetction

# Read Image
im = cv2.imread("/Users/pu/Documents/work/data/my_test_data/img/40.jpg")
size = im.shape
land_detector = LandmarksDetction()
landmarks = land_detector.face_detection(im)
key_points = [30, 8, 36, 45, 48, 54]
# 2D image points. If you change the image, you need to change vector
image_points = np.array([
    (landmarks.part(key_points[0]).x, landmarks.part(key_points[0]).y),  # Nose tip
    (landmarks.part(key_points[1]).x, landmarks.part(key_points[1]).y),  # Chin
    (landmarks.part(key_points[2]).x, landmarks.part(key_points[2]).y),  # Left eye left corner
    (landmarks.part(key_points[3]).x, landmarks.part(key_points[3]).y),  # Right eye right corne
    (landmarks.part(key_points[4]).x, landmarks.part(key_points[4]).y),  # Left Mouth corner
    (landmarks.part(key_points[5]).x, landmarks.part(key_points[5]).y)  # Right mouth corner
], dtype="double")

# 3D model points.
model_points = np.array([
    (0.0, 0.0, 0.0),  # Nose tip
    (0.0, -330.0, -65.0),  # Chin
    (-225.0, 170.0, -135.0),  # Left eye left corner
    (225.0, 170.0, -135.0),  # Right eye right corne
    (-150.0, -150.0, -125.0),  # Left Mouth corner
    (150.0, -150.0, -125.0)  # Right mouth corner

])

# Camera internals

focal_length = size[1]
center = (size[1] / 2, size[0] / 2)
camera_matrix = np.array(
    [[focal_length, 0, center[0]],
     [0, focal_length, center[1]],
     [0, 0, 1]], dtype="double"
)

print("Camera Matrix :\n {0}".format(camera_matrix))

dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs,
                                                              flags=cv2.cv2.SOLVEPNP_ITERATIVE)

print("Rotation Vector:\n {0}".format(rotation_vector))
print("Translation Vector:\n {0}".format(translation_vector))

# Project a 3D point (0, 0, 1000.0) onto the image plane.
# We use this to draw a line sticking out of the nose


(nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector,
                                                 camera_matrix, dist_coeffs)

for p in image_points:
    cv2.circle(im, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

p1 = (int(image_points[0][0]), int(image_points[0][1]))
p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

cv2.line(im, p1, p2, (255, 0, 0), 2)

# Display image
cv2.imshow("Output", im)
cv2.waitKey(0)
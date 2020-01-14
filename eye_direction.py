import cv2
import numpy as np
import dlib


def face_detection(img):
    detector = dlib.get_frontal_face_detector()
    predictors = dlib.shape_predictor("/Users/pu/Documents/work/model/benchmark/shape_predictor_68_face_landmarks.dat")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_img)
    for face in faces:
        landmarks = predictors(gray_img, face)
    return landmarks, gray_img


class EyegazaDetection:

    def __init__(self):
        self.img_height = 0
        self.img_width = 0

    def get_gaze_ratio(self, eyepoints, facial_landmarks, gray):
        left_eye_region = np.array([(facial_landmarks.part(eyepoints[0]).x, facial_landmarks.part(eyepoints[0]).y),
                                    (facial_landmarks.part(eyepoints[1]).x, facial_landmarks.part(eyepoints[1]).y),
                                    (facial_landmarks.part(eyepoints[2]).x, facial_landmarks.part(eyepoints[2]).y),
                                    (facial_landmarks.part(eyepoints[3]).x, facial_landmarks.part(eyepoints[4]).y),
                                    (facial_landmarks.part(eyepoints[4]).x, facial_landmarks.part(eyepoints[4]).y),
                                    (facial_landmarks.part(eyepoints[5]).x, facial_landmarks.part(eyepoints[5]).y)
                                    ])
        mask = np.zeros((self.img_height, self.img_width), np.int8)
        cv2.polylines(mask, [left_eye_region], True, 255, 2)
        cv2.fillPoly(mask, [left_eye_region], 255)
        eye = cv2.bitwise_and(gray, gray, mask=mask)
        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])
        gray_eye = eye[min_y:max_y, min_x:max_x]
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
        threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
        height, width = threshold_eye.shape
        left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
        left_side_white = cv2.countNonZero(left_side_threshold)
        up_side_threshold = threshold_eye[0: int(height / 2), 0: width]
        up_side_white = cv2.countNonZero(up_side_threshold)
        right_side_threshold = threshold_eye[0:height, int(width / 2): width]
        right_side_white = cv2.countNonZero(right_side_threshold)
        down_side_threshold = threshold_eye[int(height / 2): height, 0: width]
        down_side_white = cv2.countNonZero(down_side_threshold)

        if left_side_white == 0:
            gaze_ratio_hor = 1
        elif right_side_white == 0:
            gaze_ratio_hor = 1.3
        else:
            gaze_ratio_hor = left_side_white / right_side_white
        if up_side_white == 0:
            gaze_ratio_por = 1
        elif down_side_white == 0:
            gaze_ratio_por = 1.3
        else:
            gaze_ratio_por = up_side_white / down_side_white
        return gaze_ratio_hor, gaze_ratio_por

if __name__ == "__main__":
    img = cv2.imread('/Users/pu/Documents/work/data/my_test_data/img/40.jpg')
    eyegaza = EyegazaDetection()
    eyegaza.img_height, eyegaza.img_width, _ = img.shape
    landmarks, gray_img = face_detection(img)
    gaze_ratio_left_eye = eyegaza.get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, gray_img)
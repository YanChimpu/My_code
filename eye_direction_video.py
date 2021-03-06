import cv2
import dlib
import numpy as np
from math import hypot

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_length / ver_line_length
    return ratio


def get_gaze_ratio(eyepoints, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eyepoints[0]).x, facial_landmarks.part(eyepoints[0]).y),
                                (facial_landmarks.part(eyepoints[1]).x, facial_landmarks.part(eyepoints[1]).y),
                                (facial_landmarks.part(eyepoints[2]).x, facial_landmarks.part(eyepoints[2]).y),
                                (facial_landmarks.part(eyepoints[3]).x, facial_landmarks.part(eyepoints[4]).y),
                                (facial_landmarks.part(eyepoints[4]).x, facial_landmarks.part(eyepoints[4]).y),
                                (facial_landmarks.part(eyepoints[5]).x, facial_landmarks.part(eyepoints[5]).y)
                                ])

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.int8)

    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y:max_y, min_x:max_x]
    # gray_eye=cv2.cvtColor(eye,cv2.COLOR_BGR2GRAY)
    _, threshold_eye = cv2.threshold(gray_eye, 100, 255, cv2.THRESH_BINARY)
    threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
    # cv2.imshow("Threshold", threshold_eye)


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


if __name__ == '__main__':
    # cap = cv2.VideoCapture("/Users/pu/Documents/work/test.mp4")
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    detector = dlib.get_frontal_face_detector()
    predictors = dlib.shape_predictor("/Users/pu/Documents/work/model/benchmark/shape_predictor_68_face_landmarks.dat")
    while True:
        _, frame = cap.read()
        new_frame = np.zeros((500, 500, 3))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictors(gray, face)

            # Detect Blinking
            # left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            # right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            # blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
            # if blinking_ratio > 5.7:
            #     cv2.putText(frame, "Blinking", (50, 150), font, 7, (255, 0, 0), 3)
            _, gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            _, gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
            gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye) / 2
            eye_points_left = [36, 37, 38, 39, 40, 41]
            eye_points_right = [42, 43, 44, 45, 46, 47]
            for i in range(len(eye_points_left)):
                (a, b) = (landmarks.part(eye_points_left[i]).x, landmarks.part(eye_points_left[i]).y)
                (c, d) = (landmarks.part(eye_points_right[i]).x, landmarks.part(eye_points_right[i]).y)
                cv2.circle(frame, (a, b), 1, (0, 0, 255), -1)  # 画图
                cv2.circle(frame, (c, d), 1, (0, 0, 255), -1)
            if gaze_ratio <= 0.4:
                cv2.putText(frame, str("UP"), (50, 100), font, 2, (0, 0, 255), 3)
                new_frame[:] = (0, 0, 255)
            elif 0.4 < gaze_ratio < 1.05:
                cv2.putText(frame, str("CENTER"), (50, 100), font, 2, (0, 255, 0), 3)
                new_frame[:] = (0, 255, 0)
            else:
                cv2.putText(frame, str("DOWN"), (50, 100), font, 2, (0, 0, 255), 3)
                new_frame[:] = (255, 0, 0)

            # if gaze_ratio <= 0.45:
            #     cv2.putText(frame, str("RIGHT"), (50, 100), font, 2, (0, 0, 255), 3)
            #     new_frame[:] = (0, 0, 255)
            # elif 0.45 < gaze_ratio < 2.0:
            #     cv2.putText(frame, str("CENTER"), (50, 100), font, 2, (0, 255, 0), 3)
            #     new_frame[:] = (0, 255, 0)
            # else:
            #     cv2.putText(frame, str("LEFT"), (50, 100), font, 2, (255, 0, 0), 3)
            #     new_frame[:] = (255, 0, 0)

        cv2.imshow("Frame", frame)
        cv2.imshow("New Frame", new_frame)
        key = cv2.waitKey(1)

        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
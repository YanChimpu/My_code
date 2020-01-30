import cv2
import dlib


class LandmarksDetction():

    def face_detection(self, img):
        detector = dlib.get_frontal_face_detector()
        predictors = dlib.shape_predictor("/Users/pu/Documents/work/model/benchmark/shape_predictor_68_face_landmarks"
                                          ".dat")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_img)
        for face in faces:
            landmarks = predictors(gray_img, face)
        return landmarks


if __name__ == "__main__":
    img = cv2.imread("/Users/pu/Documents/work/data/my_test_data/img/40.jpg")
    ld = LandmarksDetction()
    landmarks = ld.face_detection(img)
    for i in range(68):
        (a, b) = (landmarks.part(i).x, landmarks.part(i).y)
        cv2.circle(img, (a, b), 3, (0, 0, 255), -1)  # 画图
        # cv2.putText(img, str(i), (a, b), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
        #         (0,255,0), 1)
    cv2.imshow("Output", img)
    cv2.waitKey(0)
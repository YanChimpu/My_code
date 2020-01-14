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
    for points in landmarks:

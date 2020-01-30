import face_recognition
import cv2


img = cv2.imread("1.jpg")
face = face_recognition.load_image_file("1.jpg")
face_landmarks_list = face_recognition.face_landmarks(face)
for face in face_landmarks_list:
    for face_part in face:
        for point in face[face_part]:
            cv2.circle(img, point, 3, (0, 0, 255), -1)  # 画图
cv2.imshow("Output", img)
cv2.waitKey(0)

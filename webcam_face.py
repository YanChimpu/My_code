# import face_recognition
# import cv2
#
#
# if __name__ == '__main__':
#     print('hello')
#     video = cv2.VideoCapture('webcam')
#     img, ret = video.read()
    # while True:
    #     face = face_recognition.load_image_file(img)
    #     face_landmarks_list = face_recognition.face_landmarks(face)
    #     for face in face_landmarks_list:
    #         for face_part in face:
    #             for point in face[face_part]:
    #                 cv2.circle(img, point, 3, (0, 0, 255), -1)  # 画图
    #     cv2.imshow("Output", img)
    #     img, ret = video.read()
    #     k = cv2.waitKey(1)
    #
    #     if k == ord('s'):
    #         print('222222')
    #         print(video.get(3))
    #         print(video.get(4))
    #     elif k == ord('q'):
    #         print('完成')
    #         break
    #     video.release()
    # cv2.destoryAllWindows()

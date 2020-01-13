import cv2


class FrameExtracter():
    def __init__(self):
        self.video_path = ''
        self.img_sava_path = ''
        self.img_name = 0

    def get_all_frames(self):
        video = cv2.VideoCapture(self.video_path)
        ret, img = video.read()
        img_name = self.img_name
        while ret:
            img_name_str = str(img_name) + '.jpg'
            cv2.imwrite(self.img_sava_path + img_name_str, img)
            img_name += 1
            ret, img = video.read()


if __name__ == "__main__":
    frame_extracter = FrameExtracter()
    frame_extracter.video_path = '/Users/pu/Documents/work/data/my_test_data/video/eyegaza_test.mp4'
    frame_extracter.img_sava_path = '/Users/pu/Documents/work/data/my_test_data/img/'
    frame_extracter.get_all_frames()
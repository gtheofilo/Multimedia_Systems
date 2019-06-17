# System Imports
import os

# Third Party Imports
import cv2


class VideoToFramesConverter():

    def __init__(self, sample_path, save_path):

        self.sample_path = sample_path
        self.save_path = save_path
        self.video_capture = cv2.VideoCapture(self.sample_path)
        self.width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        cv2
        self.height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.size = self.width, self.height

    def create_frames(self):

        success , image = self.video_capture.read()
        count = 0
        while success:
            cv2.imwrite(os.path.join(self.save_path, f'frame{count}.jpg'),image)
            success,image = self.video_capture.read()
            count += 1


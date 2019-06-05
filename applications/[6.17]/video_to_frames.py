import cv2

class VideoToFramesConverter():

    def __init__(self, path):

        self.path = path
        self.video_capture = cv2.VideoCapture(self.path)

    def create_frames(self):

        success , image = self.video_capture.read()
        count = 0
        while success:
          cv2.imwrite("frame%d.jpg" % count, image)
          success,image = self.video_capture.read()
          print('Read a new frame: ', success)
          count += 1
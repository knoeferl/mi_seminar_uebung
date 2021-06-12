import os

import cv2


class ReadFromVideo(object):
    def __init__(self, video_path, sample_interval=1):
        ''' A video reader class for reading video frames from video.
        Arguments:
            video_path
            sample_interval {int}: sample every kth image.
        '''
        if not os.path.exists(video_path):
            raise IOError("Video not exist: " + video_path)
        assert isinstance(sample_interval, int) and sample_interval >= 1
        self.cnt_imgs = 0
        self._is_stoped = False
        self._video = cv2.VideoCapture(video_path)
        ret, image = self._video.read()
        self._next_image = image
        self._sample_interval = sample_interval
        self._fps = self.get_fps()
        if not self._fps >= 0.0001:
            import warnings
            warnings.warn("Invalid fps of video: {}".format(video_path))

    def has_image(self):
        return self._next_image is not None

    def get_curr_video_time(self):
        return 1.0 / self._fps * self.cnt_imgs

    def read_image(self):
        image = self._next_image
        for i in range(self._sample_interval):
            if self._video.isOpened():
                ret, frame = self._video.read()
                self._next_image = frame
            else:
                self._next_image = None
                break
        self.cnt_imgs += 1
        return image

    def stop(self):
        self._video.release()
        self._is_stoped = True

    def __del__(self):
        if not self._is_stoped:
            self.stop()

    def get_fps(self):

        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        # With webcam get(CV_CAP_PROP_FPS) does not work.
        # Let's see for ourselves.

        # Get video properties
        if int(major_ver) < 3:
            fps = self._video.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = self._video.get(cv2.CAP_PROP_FPS)
        return fps


class VideoWriter(object):
    def __init__(self, video_path, framerate):

        # -- Settings
        self._video_path = video_path
        self._framerate = framerate

        # -- Variables
        self._cnt_img = 0
        # initialize later when the 1st image comes
        self._video_writer = None
        self._width = None
        self._height = None

        # -- Create output folder
        folder = os.path.dirname(video_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def write(self, img):
        self._cnt_img += 1
        if self._cnt_img == 1:  # initialize the video writer
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # define the codec
            self._width = img.shape[1]
            self._height = img.shape[0]
            self._video_writer = cv2.VideoWriter(
                self._video_path, fourcc, self._framerate, (self._width, self._height))
        self._video_writer.write(img)

    def stop(self):
        self.__del__()

    def __del__(self):
        if self._cnt_img > 0:
            self._video_writer.release()
            print("Complete writing {}fps and {}s video to {}".format(
                self._framerate, self._cnt_img / self._framerate, self._video_path))


class ImageDisplayer(object):
    ''' A simple wrapper of using cv2.imshow to display image '''

    def __init__(self):
        self._window_name = "cv2_display_window"
        cv2.namedWindow(self._window_name, cv2.WINDOW_NORMAL)

    def display(self, image, wait_key_ms=1):
        cv2.imshow(self._window_name, image)
        cv2.waitKey(wait_key_ms)

    def __del__(self):
        cv2.destroyWindow(self._window_name)


def draw_scores_onto_image(img_disp, scores, action_labels):
    if scores is None:
        return

    for i in range(-1, len(action_labels)):

        FONT_SIZE = 0.7
        TXT_X = 20
        TXT_Y = 150 + i * 30
        COLOR_INTENSITY = 255
        possibility = scores[i]

        if i == -1:
            s = "prediction:"
        else:
            label = action_labels[i]
            s = "{:}: {:3.2f}".format(label, possibility)
            COLOR_INTENSITY *= (0.0 + 1.0 * possibility) ** 0.5

        cv2.putText(img_disp, text=s, org=(TXT_X, TXT_Y),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=FONT_SIZE,
                    color=(0, 0, int(COLOR_INTENSITY)), thickness=2)
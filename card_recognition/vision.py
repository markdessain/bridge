import cv2

from utils import create_thresh, get_contours, warp_contour_from_image, resize_into_square


class Vision:

    def __init__(self):
        pass

    def update(self):
        self.frame = self.get_frame()
        self.frame_thresh = create_thresh(self.frame)
        self.preview_thresh = resize_into_square(self.frame_thresh, 150)

        self.found_card, self.card, self.card_thresh = self.get_card()

    def get_frame(self):
        pass

    def get_card(self):
        try:
            contours = get_contours(self.frame_thresh, 1)

            if contours:
                card = warp_contour_from_image(self.frame, contours[0], 300)
                card = card[0:40, 0:90]
                card_thresh = create_thresh(card)

                # card = cv2.resize(card, (45, 20))
                # card_thresh = cv2.resize(card_thresh, (45, 20))
                return True, card, card_thresh
        except Exception as e:
            pass

        return False, None, None


class Webcam(Vision):

    def __init__(self):
        # self.vc = cv2.VideoCapture(0)
        self.vc = cv2.VideoCapture('http://192.168.0.10:8080/video?x.mjpeg')

    def get_frame(self):
        _, frame = self.vc.read()

        return frame

    def preview(self):
        if self.found_card:
            p = self.card_thresh
        else:
            p = self.preview_thresh

        return p
        # return cv2.resize(p, (45, 20))

class Trainer(Vision):

    def __init__(self, image):
        self.image = image

    def get_frame(self):
        return cv2.cvtColor( self.image, cv2.COLOR_BGR2RGB)

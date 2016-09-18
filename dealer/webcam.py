import cv2


class TrainingController:

    def __init__(self):
        self.webcam = Webcam()
        self.selected_suit = None
        self.selected_rank = None

    def update(self):
        self.webcam.update()

    def select_rank(self, rank):
        self.selected_rank = rank

        if self.selected_rank and self.selected_suit:
            self.selected_rank = None
            self.selected_suit = None

    def select_suit(self, suit):
        self.selected_suit = suit

        if self.selected_rank and self.selected_suit:
            self.selected_rank = None
            self.selected_suit = None


class Webcam:

    def __init__(self):
        # self.vc = cv2.VideoCapture(0)
        self.vc = cv2.VideoCapture('http://192.168.1.105:8080/video?x.mjpeg')

    def update(self):
        _, self.frame = self.vc.read()

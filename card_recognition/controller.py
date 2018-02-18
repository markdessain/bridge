import random
import string
import threading
from collections import Counter

import cv2

from vision import Webcam
from model import Model
from utils import create_thresh, image_diff, warp_contour_from_image


class Controller:

    def __init__(self):
        self.webcam = Webcam()
        self.selected_suit = None
        self.selected_rank = None

        self.running = False

    def update(self):
        self.webcam.update()

    def ready(self):
        return True

    def bind_return(self, event):
        pass

    def bind_key(self, event):
        if event.char == ' ':
            self.running = not self.running
        elif event.char.upper() in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
            self.selected_rank = event.char.upper()
        elif event.char.upper() in ['C', 'D', 'H', 'S']:
            self.selected_suit = {'C': 'Club', 'D': 'Dimmand', 'H': 'Heart', 'S': 'Spade'}[event.char.upper()]
        self.run_if_ready()

    def select_rank(self, rank):
        self.selected_rank = rank
        self.run_if_ready()

    def select_suit(self, suit):
        self.selected_suit = suit
        self.run_if_ready()

    def select_misc(self, misc):
        if misc == 'Start':
            self.running = True
        elif misc == 'Stop':
            self.running = False
        self.run_if_ready()

    def run_if_ready(self):
        if self.ready():
            self.run()


class LiveController(Controller):

    def __init__(self):
        super().__init__()
        self.counter = []
        self.model = Model.load()

    def update(self):
        super().update()

        if self.webcam.found_card:
            guess = self.model.predict([self.webcam.card_thresh.flatten()])
            if len(self.counter) == 10:
                self.counter.pop()
            self.counter.insert(0, guess[0])

    def get_guess(self):
        for c in self.counter:
            if c:
                yield c
            else:
                yield 'NA'
        for c in range(10 - len(self.counter)):
            yield '  '

    def run(self):
        pass


class CaptureController(Controller):

    def ready(self):
        return self.selected_rank and self.selected_suit

    def run(self):
        def worker():
            i = 0
            while self.running and self.ready():
                import time
                time.sleep(1)
                cv2.imwrite('./tmp/capture/%s%s_%s.png' % (
                    self.selected_rank,
                    self.selected_suit[0],
                    str(i)
                ), self.webcam.frame)

                i += 1

        t = threading.Thread(target=worker)
        t.start()

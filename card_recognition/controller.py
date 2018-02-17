import random
import string
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

        self.counter = []

        ranks = [
            'A',
            'K',
            'Q',
            'J',
            'T',
            '9',
            '8',
            '7',
            '6',
            '5',
            '4',
            '3',
            '2',
        ]

        suits = [
            # 'H',
            'S',
            # 'D',
            # 'C'
        ]
        classes = sum([['%s%s' % (rank, suit) for rank in ranks] for suit in suits], [])

        self.model = Model(classes)
        self.model.train()

        self.auto = False

    def update(self):
        self.webcam.update()

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

    def bind_return(self, event):
        pass

    def bind_key(self, event):
        if event.char == ' ':
            self.auto = not self.auto
        elif event.char.upper() in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
            self.selected_rank = event.char.upper()
            if self.selected_rank and self.selected_suit:
                self.run()
        elif event.char.upper() in ['C', 'D', 'H', 'S']:
            self.selected_suit = {'C': 'Club', 'D': 'Dimmand', 'H': 'Heart', 'S': 'Spade'}[event.char.upper()]
            if self.selected_rank and self.selected_suit:
                self.run()

    def select_rank(self, rank):
        self.selected_rank = rank

        if self.selected_rank and self.selected_suit:
            self.run()

    def select_suit(self, suit):
        self.selected_suit = suit

        if self.selected_rank and self.selected_suit:
            self.run()

    def select_misc(self, misc):
        if misc == 'Start':
            self.auto = True
        elif misc == 'Stop':
            self.auto = False

    def run(self):
        cv2.imwrite('card_recognition/training_images/cards/%s%s_%s.png' % (
            self.selected_rank,
            self.selected_suit[0],
            ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
        ), self.webcam.frame)

        with open('card_recognition/training_images/data.csv', 'a') as f:
            f.write('%s%s|%s' % (self.selected_rank, self.selected_suit[0], list(self.webcam.card_thresh.flatten())))
            f.write('\n')

        self.model.partial_fit([self.webcam.card_thresh.flatten()], ['%s%s' % (self.selected_rank, self.selected_suit[0])])

        self.selected_suit = None
        self.selected_rank = None

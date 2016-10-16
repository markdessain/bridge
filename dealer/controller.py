import random
import string
from collections import Counter

import cv2

from vision import Webcam
from recognition import Recognition
from deck_builder import DeckBuilder
from utils import create_thresh, image_diff, warp_contour_from_image

class Controller:

    def __init__(self):
        self.webcam = Webcam()
        self.selected_suit = None
        self.selected_rank = None

        self.counter = []

        self.deck_builder = DeckBuilder()
        self.recognition = Recognition(self.deck_builder, self.webcam)
        self.recognition.train()

        self.auto = False

    def update(self):
        self.webcam.update()

        if self.webcam.found_card:
            guess = self.recognition.guess()
            if len(self.counter) == 10:
                self.counter.pop()
            self.counter.insert(0, guess)

        c = list(filter(None, self.counter))

        if self.auto and len(c) == 10 and len(set(c)) == 1:
            self.deck_builder.select(c[0])
            self.selected_suit = None
            self.selected_rank = None

    def previous_cards(self, n):
        return self.deck_builder.deck[-n:]

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
        elif event.char == '\x08':
            self.auto = not self.auto
            self.deck_builder.undo()

    def select_rank(self, rank):
        self.selected_rank = rank

        if self.selected_rank and self.selected_suit:
            self.run()

    def select_suit(self, suit):
        self.selected_suit = suit

        if self.selected_rank and self.selected_suit:
            self.run()

    def select_misc(self, misc):
        if misc == 'Undo':
            self.deck_builder.undo()
        elif misc == 'Start':
            self.auto = True
        elif misc == 'Stop':
            self.auto = False

    def run(self):
        cv2.imwrite('training_images/cards/%s%s_%s.png' % (
            self.selected_rank,
            self.selected_suit[0],
            ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
        ), self.webcam.frame)

        self.deck_builder.select('%s%s' % (self.selected_rank, self.selected_suit[0]))

        self.selected_suit = None
        self.selected_rank = None

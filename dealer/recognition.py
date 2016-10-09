import glob
import multiprocessing

import cv2

from utils import image_diff, score_diff, create_thresh, is_red

from vision import Trainer


class Recognition:

    def __init__(self, deck_builder, webcam):
        self.training_cards = {}
        self.training_suits = {}
        self.deck_builder = deck_builder
        self.webcam = webcam

        self.pool = multiprocessing.Pool(4)

    def train(self):
        self.training_cards = list(self._train_cards())
        self.training_suits = dict(self._train_suits())

    def _train_cards(self):
        for card in glob.glob('training_images/cards/*'):
            value = card.split('/')[-1].split('.')[0].split('_')[0]
            frame = cv2.imread(card)
            trainer = Trainer(frame)
            trainer.update()
            output = trainer.card_thresh
            yield (value, output)

    def _train_suits(self):
        for card in glob.glob('training_images/suits/*'):
            value = card.split('/')[-1].split('.')[0].split('_')[0]
            frame = cv2.imread(card)
            frame = create_thresh(frame)
            output = cv2.Canny(frame, 50, 200)
            yield (value, output)

    def guess(self):

        output = self.webcam.card_thresh

        if is_red(self.webcam.card):
            suits = ['D', 'H']
        else:
            suits = ['C', 'S']

        results = []

        check = []
        for value, training in self.training_cards:
            if value not in self.deck_builder.deck[:-1] and value[1] in suits:
                check.append((value, output, training))

        results = self.pool.map(run, check)

        return sorted(results, key=lambda x: x[1])[0][0]


def run(data):
    value, a, b = data
    diff = image_diff(a, b)
    score = score_diff(diff)
    return (value, score)

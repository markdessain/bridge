import glob

import cv2

from utils import process, image_diff, score_diff


class Recognition:

    def __init__(self, deck_builder):
        self.training_set = {}
        self.deck_builder = deck_builder

    def train(self):
        for card in glob.glob('training_images/cards/*'):

            value = card.split('/')[1].split('.')[0]
            frame = cv2.imread(card)
            output = process(frame)

            self.training_set[value] = output

    def guess(self, frame):

        output = process(frame)

        results = []

        for value, training in self.training_set.items():
            if value not in self.deck_builder.deck:
                diff = image_diff(output, training)
                score = score_diff(diff)

                results.append((value, score))

        return sorted(results, key=lambda x: x[1])[0][0]

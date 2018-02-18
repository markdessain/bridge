import pickle
from sklearn.neural_network import MLPClassifier

import glob
import cv2
from vision import Trainer
from PIL import Image, ImageTk


class Model:

    def __init__(self):
        self.mlp = MLPClassifier(hidden_layer_sizes=(40,), max_iter=400, epsilon=0.0001)

    def fit(self, X, y):
        self.mlp.fit(X, y)

    def predict(self, X):
        return self.mlp.predict(X)

    def describe(self):
        print(self.mlp.loss_curve_)

    def save(self):
        pickle.dump(self, open('./tmp/model.pkl', 'wb'))

    @staticmethod
    def load():
        return pickle.load(open('./tmp/model.pkl', 'rb'))



def features():
    for card in glob.glob('./tmp/capture/*'):
        value = card.split('/')[-1].split('.')[0].split('_')[0]
        frame = cv2.imread(card)
        trainer = Trainer(frame)
        trainer.update()
        output = trainer.card_thresh

        try:
            img = Image.fromarray(output)
            img.save('./tmp/clean/%s' % card.split('/')[-1])
        except:
            print(card)


def train():
    model = Model()

    Xs = []
    ys = []

    for card in glob.glob('./tmp/clean/*'):
        value = card.split('/')[-1].split('.')[0].split('_')[0]
        frame = cv2.imread(card)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        Xs.append(list(frame.flatten()))
        ys.append(value)

    model.fit(Xs, ys)
    model.describe()
    model.save()

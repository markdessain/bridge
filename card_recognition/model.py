import pickle
from sklearn.neural_network import MLPClassifier


class Model:

    def __init__(self, classes):
        self.mlp = MLPClassifier(hidden_layer_sizes=(500,), max_iter=400, epsilon=0.0001)
        self.classes = classes
        self.first_time = True

    def fit(self, X, y):
        self.mlp.fit(X, y)

    def partial_fit(self, X, y):
        if self.first_time:
            self.mlp.partial_fit(X, y, self.classes)
            self.first_time = False
        else:
            self.mlp.partial_fit(X, y)

    def predict(self, X):
        return self.mlp.predict(X)

    def describe(self):
        print(self.mlp.loss_curve_)

    def train(self):

        import glob
        import cv2
        from vision import Trainer
        from PIL import Image, ImageTk

        with open('card_recognition/training_images/data.csv', 'w') as f:
            for card in glob.glob('card_recognition/training_images/cards/*'):
                value = card.split('/')[-1].split('.')[0].split('_')[0]
                frame = cv2.imread(card)
                trainer = Trainer(frame)
                trainer.update()
                output = trainer.card_thresh

                try:
                    img = Image.fromarray(output)
                    img.save('./tmp/clean/%s' % card.split('/')[-1])

                    output = list(output.flatten())
                    f.write('%s|%s' % (value, output))
                    f.write('\n')

                    self.partial_fit([output], [value])
                except:
                    print(card)

        self.describe()

    def save(self):
        pickle.dump(self, open('./tmp/model.pkl', 'wb'))

    @staticmethod
    def load():
        return pickle.load(open('./tmp/model.pkl', 'rb'))

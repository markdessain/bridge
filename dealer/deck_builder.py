from collections import Counter


class DeckBuilder:

    def __init__(self):
        self.counter = Counter()
        self.deck = []

    def update(self):
        if sum(self.counter.values()) == 10:
            print(self.counter)
            self.counter.clear()

    def add(self, card):
        self.counter[card] += 1

    def select(self):
        card = self.counter.most_common()[0][0]
        if card not in self.deck:
            self.deck.append(card)

        if len(self.deck) == 13:
            print('**************')
            print('*** Hand 1 ***')
            print('**************')

        if len(self.deck) == 26:
            print('**************')
            print('*** Hand 2 ***')
            print('**************')

        if len(self.deck) == 39:
            print('**************')
            print('*** Hand 3 ***')
            print('**************')

        if len(self.deck) == 52:
            print('**************')
            print('*** Hand 4 ***')
            print('**************')
            self.save()
            self.counter.clear()
            self.deck = []

    def save(self):
        print(self.deck[0:13])
        print(self.deck[13:26])
        print(self.deck[26:39])
        print(self.deck[39:52])

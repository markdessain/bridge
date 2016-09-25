from functools import partial
from collections import Counter

import random
import string
import cv2
import tkinter as tk
from PIL import Image, ImageTk

from utils import create_thresh, image_diff, get_almost_square_contours, warp_contour_from_image
from recognition import Recognition
from deck_builder import DeckBuilder
from vision import Webcam


class UI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.preview = None
        self.guess = None

        self.previous_cards = tk.Label(self)

        self.buttons = {'suits': {}, 'ranks': {}, 'misc': {}}
        self.controls = self.build_controls()
        self.display = self.build_display()

    def show(self):
        for section in [
            self.controls,
            self.display,
            self.previous_cards
        ]:
            section.pack()

        self.bind("<Return>", self.controller.bind_return)
        self.bind("<Key>", self.controller.bind_key)
        self.mainloop()

    def mainloop(self):
        def update():
            self.controller.update()
            self.update_guess()
            self.update_previous_cards()
            self.update_preview()
            self.update_buttons()
            self.after(1, update)
        update()
        super().mainloop()

    def update_guess(self):
        self.guess['text'] = ', '.join(self.controller.get_guess())

    def update_previous_cards(self):
        self.previous_cards['text'] = self.controller.previous_cards(13)

    def update_preview(self):
        cv2image = self.controller.webcam.preview()
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.preview.imgtk = imgtk
        self.preview.configure(image=imgtk)

    def update_buttons(self):
        self.reset_buttons(self.buttons['suits'].values())
        self.reset_buttons(self.buttons['ranks'].values())
        self.reset_buttons(self.buttons['misc'].values())

        if self.controller.selected_suit:
            self.buttons['suits'][self.controller.selected_suit].config(state=tk.DISABLED)
        if self.controller.selected_rank:
            self.buttons['ranks'][self.controller.selected_rank].config(state=tk.DISABLED)

        if self.controller.auto:
            self.buttons['misc']['Start'].config(state=tk.DISABLED)
        else:
            self.buttons['misc']['Stop'].config(state=tk.DISABLED)

    def build_controls(self):
        frame = tk.Frame(self)

        for suit in ['Club', 'Dimmand', 'Heart', 'Spade']:
            command = partial(self.controller.select_suit, suit)
            b = tk.Button(frame, text=suit, command=command)
            b.pack(side=tk.LEFT)
            self.buttons['suits'][suit] = b

        for rank in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
            command = partial(self.controller.select_rank, rank)
            b = tk.Button(frame, text=rank, command=command)
            b.pack(side=tk.LEFT)
            self.buttons['ranks'][rank] = b

        for misc in ['Undo', 'Start', 'Stop']:
            command = partial(self.controller.select_misc, misc)
            b = tk.Button(frame, text=misc, command=command)
            b.pack(side=tk.LEFT)
            self.buttons['misc'][misc] = b

        return frame

    def build_display(self):
        frame = tk.Frame(self)

        self.preview = tk.Label(frame)
        self.guess = tk.Label(frame, text='??', font=("Helvetica", 36))

        self.preview.pack(side=tk.LEFT)
        self.guess.pack(side=tk.LEFT)

        return frame

    def reset_buttons(self, buttons):
        for button in buttons:
            button.config(state=tk.NORMAL)


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

from functools import partial

import tkinter as tk
from PIL import Image, ImageTk

from controller import LiveController, CaptureController


class UI(tk.Tk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.preview = None
        self.card = None
        self.guess = None

        self.buttons = {'suits': {}, 'ranks': {}, 'misc': {}}
        self.controls = self.build_controls()
        self.display = self.build_display()

    def show(self):
        for section in [
            self.controls,
            self.display
        ]:
            section.pack()

        self.bind("<Return>", self.controller.bind_return)
        self.bind("<Key>", self.controller.bind_key)
        self.mainloop()

    def update_preview(self):
        cv2image = self.controller.webcam.preview_thresh
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.preview.imgtk = imgtk
        self.preview.configure(image=imgtk)

    def update_card(self):
        try:
            cv2image = self.controller.webcam.card_thresh
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.card.imgtk = imgtk
            self.card.configure(image=imgtk)
        except:
            self.card.imgtk = None
            self.card.configure(image=None)

    def update_buttons(self):
        self.reset_buttons(self.buttons['suits'].values())
        self.reset_buttons(self.buttons['ranks'].values())
        self.reset_buttons(self.buttons['misc'].values())

        if self.controller.selected_suit:
            self.buttons['suits'][self.controller.selected_suit].config(state=tk.DISABLED)
        if self.controller.selected_rank:
            self.buttons['ranks'][self.controller.selected_rank].config(state=tk.DISABLED)

        if self.controller.running:
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

    def reset_buttons(self, buttons):
        for button in buttons:
            button.config(state=tk.NORMAL)



class CatpureUI(UI):
    def __init__(self):
        super().__init__(CaptureController())

    def build_display(self):
        frame = tk.Frame(self)

        self.preview = tk.Label(frame)
        self.preview.pack(side=tk.LEFT)

        self.card = tk.Label(frame)
        self.card.pack(side=tk.LEFT)

        return frame

    def update_buttons(self):
        super().update_buttons()
        self.buttons['misc']['Undo'].config(state=tk.DISABLED)

    def mainloop(self):
        def update():
            self.controller.update()
            self.update_preview()
            self.update_card()
            self.update_buttons()
            self.after(1, update)
        update()
        super().mainloop()


class LiveUI(UI):
    def __init__(self):
        super().__init__(LiveController())

    def update_guess(self):
        self.guess['text'] = ', '.join(self.controller.get_guess())

    def build_display(self):
        frame = tk.Frame(self)

        self.preview = tk.Label(frame)
        self.guess = tk.Label(frame, text='??', font=("Helvetica", 36))

        self.card = tk.Label(frame)

        self.preview.pack(side=tk.LEFT)
        self.card.pack(side=tk.LEFT)
        self.guess.pack(side=tk.LEFT)

        return frame

    def mainloop(self):
        def update():
            self.controller.update()
            self.update_guess()
            self.update_preview()
            self.update_card()
            self.update_buttons()
            self.after(1, update)
        update()
        super().mainloop()

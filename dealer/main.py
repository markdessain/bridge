
import cv2

from recognition import Recognition
from webcam import Webcam
from deck_builder import DeckBuilder

from utils import process


if __name__ == '__main__':


    c = Recognition()
    c.train()

    db = DeckBuilder()
    webcam = Webcam()


    cv2.namedWindow("preview")
    while True:
        db.update()
        webcam.update()

        frame = webcam.frame
        output = process(frame)

        try:
            db.add(c.guess(frame))
        except:
            pass

        cv2.imshow("preview", output)

        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
        if ((key == 13) or (key==32)):
            db.select()

    cv2.destroyWindow("preview")

    print(card_order)





    # ui = TrainingUI()
    # ui.show()



    # hb = HandBuilder()
    # hb.next()
    #
    #
    # c = CardRecognition()
    # c.train()
    #
    # result = c.guess(cv2.imread('training_images/4C.jpg'))
    # hb.add_card(result)
    # hb.add_card(result)
    # result = c.guess(cv2.imread('training_images/7C.jpg'))
    # hb.add_card(result)
    #
    # print(hb.current_hand())
    #
    # print(result)
    #
    # hb.show()
    #
    #


    #
    # # diff = image_diff(frame, frame_2)
    #
    # while True:
    #     output = process(frame)
    #     output_2 = process(frame_2)
    #     diff = image_diff(output, output_2)
    #
    #
    #     cv2.imshow("input", frame)
    #     cv2.imshow("output", diff)
    #
    #     key = cv2.waitKey(20)
    #     if key == 27: # exit on ESC
    #         break
    # cv2.destroyWindow("input")
    # cv2.destroyWindow("output")







# import numpy as np
# import cv2
# import tkinter
# from PIL import Image, ImageTk
#
#
# image = cv2.imread('training_1.jpg')
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray,(5,5),1000)
# flag, thresh = cv2.threshold(blur, 140, 255, cv2.THRESH_BINARY)
#
# # A root window for displaying objects
# root = tkinter.Tk()
#
# # Convert the Image object into a TkPhoto object
# im = Image.fromarray(thresh)
# imgtk = ImageTk.PhotoImage(image=im)
#
# # Put it in the display window
# tkinter.Label(root, image=imgtk).pack()
#
# root.mainloop() # Start the GUI

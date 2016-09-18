
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

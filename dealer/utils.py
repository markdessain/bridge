import cv2
import glob
import numpy as np


###############################################################################
# Utility code from
# http://git.io/vGi60A
# Thanks to author of the sudoku example for the wonderful blog posts!
###############################################################################

def rectify(h):
  h = h.reshape((4,2))
  hnew = np.zeros((4,2),dtype = np.float32)

  add = h.sum(1)
  hnew[0] = h[np.argmin(add)]
  hnew[2] = h[np.argmax(add)]

  diff = np.diff(h,axis = 1)
  hnew[1] = h[np.argmin(diff)]
  hnew[3] = h[np.argmax(diff)]

  return hnew


def create_thresh(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),1000)
    flag, thresh = cv2.threshold(blur, 140, 255, cv2.THRESH_BINARY)
    return thresh


def get_almost_square_contours(image, count):
    im2, contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[0:count]

    results = []

    for contour in contours:

        s = cv2.contourArea(contour)

        if s > 100 and s < 1000000:
            x,y,w,h = cv2.boundingRect(contour)

            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            results.append((contour))

    return results


def add_contours(image, contours):
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)


def warp_contour_from_image(image, contour, size):
    peri = cv2.arcLength(contour,True)
    approx = rectify(cv2.approxPolyDP(contour,0.02*peri,True))

    s = size
    C = np.array([ [0,0],[s-1,0],[s-1,s-1],[0,s-1] ],np.float32)

    transform = cv2.getPerspectiveTransform(approx,C)

    warp = cv2.warpPerspective(image,transform,(s,s))
    return warp


def process(image):
    """ Takes the first largest contour and will display a warped
    version of it in a 400x400 square.
    """
    thresh = create_thresh(image)
    contours = get_almost_square_contours(thresh, 1)
    # add_contours(image, contours)

    # print(len(contours))
    if contours:

        try:
            warp = warp_contour_from_image(image, contours[0], 400)
            warp_thresh = create_thresh(warp)
            # warp_contours = get_almost_square_contours(warp_thresh, 100)
            # print(len(warp_contours))
            # add_contours(warp, warp_contours)
            return warp_thresh
        except:
            print('Failed to Warp')
            return thresh
    else:
        print('No Contours')
        return thresh


def image_diff(image1, image2):
    image1 = cv2.GaussianBlur(image1, (5,5), 5)
    image2 = cv2.GaussianBlur(image2, (5,5), 5)
    diff = cv2.absdiff(image1, image2)
    diff = cv2.GaussianBlur(diff, (5,5), 5)
    # flag, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY)
    return diff


def score_diff(diff):
    return np.sum(diff)

import cv2
import sys
import numpy as np
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import pytesseract
import image as img

def getTime(im):
    DIGITS_LOOKUP = {
    	(1, 1, 1, 1, 1, 1, 1): 0,
    	(0, 0, 1, 0, 0, 1, 0): 1,
    	(1, 0, 1, 0, 0, 0, 1): 2,
        (1, 0, 1, 0, 1, 0, 1): 2,
    	(1, 0, 0, 0, 0, 1, 1): 3,
        (1, 0, 0, 1, 0, 1, 1): 3,
        (1, 0, 0, 1, 0, 1, 0): 3,
    	(0, 0, 0, 1, 1, 1, 0): 4,
        (0, 0, 0, 1, 1, 0, 0): 4,
    	(1, 1, 0, 1, 0, 1, 1): 5,
    	(1, 1, 0, 1, 1, 1, 1): 6,
    	(1, 0, 1, 0, 0, 1, 0): 7,
        (1, 0, 0, 0, 0, 0, 0): 7,
    	(1, 0, 0, 1, 1, 1, 1): 8,
    	(1, 1, 1, 1, 0, 1, 1): 9
    }
    #gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(im,(5,5),0)
    thresh = cv2.threshold(blur, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # find contours in the thresholded image, then initialize the
    # digit contours lists
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = []

    # loop over the digit area candidates
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # if the contour is sufficiently large, it must be a digit
        if w >= 5 and (h >= 10 and h <= 40):
            digitCnts.append(c)

    digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0]
    digits = []
    # loop over each of the digits
    for c in digitCnts:
    	# extract the digit ROI
    	(x, y, w, h) = cv2.boundingRect(c)
    	roi = thresh[y:y + h, x:x + w]
    	# compute the width and height of each of the 7 segments
    	# we are going to examine
    	(roiH, roiW) = roi.shape
    	(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
    	dHC = int(roiH * 0.05)

    	# define the set of 7 segments
    	segments = [
    		((0, 0), (w, dH)),	# top
    		((0, 0), (dW, h // 2)),	# top-left
    		((w - dW, 0), (w, h // 2)),	# top-right
    		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
    		((0, h // 2), (dW, h)),	# bottom-left
    		((w - dW, h // 2), (w, h)),	# bottom-right
    		((0, h - dH), (w, h))	# bottom
    	]
    	on = [0] * len(segments)
        	# loop over the segments
    	for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
    		# extract the segment ROI, count the total number of
    		# thresholded pixels in the segment, and then compute
    		# the area of the segment
    		segROI = roi[yA:yB, xA:xB]
    		total = cv2.countNonZero(segROI)
    		area = (xB - xA) * (yB - yA)

    		# if the total number of non-zero pixels is greater than
    		# 50% of the area, mark the segment as "on"
    		if total / float(area) > 0.5:
    			on[i]= 1

    	# lookup the digit and draw it on the image
    	digit = DIGITS_LOOKUP[tuple(on)]
    	digits.append(digit)
    return digits

def stringProcess(str):
    str = str[4:]
    count = 0
    index = 0
    i=0
    for c in str:
        if c == '.':
            count = count + 1
            index=i
        i = i+1

    if count > 1:
        return str[:index]
    else:
        return str

def getMoney(im):
    #im = cv2.imread("money.jpg")
    h,w = im.shape
    im_Size = cv2.resize(im,(w*3,h*3))
    #gray = cv2.cvtColor(im_Size, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(im_Size, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"
    str = pytesseract.image_to_string(thresh)
    return float(stringProcess(str))*1000
    #cv2.imshow("MONEY",thresh)
    #cv2.imshow("MONEY2",im)
    #cv2.imshow("MONEY2",im_Size)
    #cv2.waitKey(0)

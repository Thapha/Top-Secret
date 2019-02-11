from PIL import ImageGrab
import numpy as np
import cv2
import constant as c

h = c.HEIGHT
w = c.WIDTH

frame_w = w*39/100
frame_h = h
def getFrame():
    img = ImageGrab.grab(bbox=(w*18/100,0,w*39/100,h)) # get the dragon tiger game box
                                                       # Box: 18% 0 39% 100% (x,y,w(533),h)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Capturing frame", frame)
    return frame

def getDetails():
    im = getFrame()
    crop_im_time = im[int(frame_h*39/100):int(frame_h*42.96/100), int(frame_w*2.8/100):int(frame_w*11.25/100)]
    crop_im_money = im[int(frame_h*91.14/100):int(frame_h*93.75/100), int(frame_w*13.13/100):int(frame_w*30/100)]
    #cv2.imshow("Money",crop_im_time)
    #cv2.imshow("Money",crop_im_money)
    #cv2.waitKey(0)
    #cv2.imwrite("money.jpg",crop_im_money)
    return crop_im_time,crop_im_money

getDetails()

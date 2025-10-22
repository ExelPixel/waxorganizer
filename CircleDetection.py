import sys
import cv2 as cv
import config as cfg
import numpy as np
def main(imageInput):

    if imageInput is None:
        print ('Error opening image!')
        return -1 #TODO: Change this

    # height, width = src.shape
    # newWidth = int(width * 1)
    # newHeight = int(height * 1)
    # resized = cv.resize(src, (newWidth, newHeight), interpolation=cv.INTER_AREA)
    gray = cv.medianBlur(imageInput, 5)
    # gray = cv.GaussianBlur(gray, 7, 1.5, 1.5) 

    imgHeigth, imgWidth = gray.shape
    # https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d params
    circles = cv.HoughCircles(
        gray,
        cv.HOUGH_GRADIENT,
        dp=5,
        minDist=imgHeigth,
        param1=300,
        param2=1,
        minRadius=int(imgWidth/4),
        maxRadius=0
    )
    
    assert circles is not None, "no label outline was found"

    circles = np.uint16(np.around(circles))
    if cfg.debugCircleDetection:
        debug_img = imageInput.copy()
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(debug_img, center, 1, (0, 0, 0), 50)
            # circle outline
            radius = i[2]
            cv.circle(debug_img, center, radius, (0, 0, 0), 10)
        
        cv.namedWindow("detected circles", cv.WINDOW_NORMAL)
        cv.resizeWindow("detected circles", 600, 800)
        cv.imshow("detected circles", debug_img)
        cv.waitKey(0)
    
    return circles

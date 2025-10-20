import sys
import cv2 as cv
import config as cfg
import numpy as np
def main(imageInput):
    
    src = imageInput

    if src is None:
        print ('Error opening image!')
        return -1 #TODO: Change this

    height, width = src.shape
    newWidth = int(width * 1)
    newHeight = int(height * 1)
    resized = cv.resize(src, (newWidth, newHeight), interpolation=cv.INTER_AREA)
    gray = cv.medianBlur(resized, 5)
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
    
    assert circles is not None, "no label was found"

    if cfg.debugCircleDetection:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(resized, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(resized, center, radius, (255, 0, 255), 3)
        
        cv.namedWindow("detected circles", cv.WINDOW_NORMAL)
        cv.resizeWindow("detected circles", 600, 800)
        cv.imshow("detected circles", resized)
        cv.waitKey(0)
    
    return circles

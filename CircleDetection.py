import sys
import cv2 as cv
import numpy as np
def main(imageInput):
    
    # default_file = 'smarties.png'
    # filename = argv[0] if len(argv) > 0 else default_file
    # # Loads an image
    # src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)
    # # Check if image is loaded fine

    src = imageInput

    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' '] \n')
        return -1
    
    
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    
    
    gray = cv.medianBlur(gray, 5)
    
    
    rows = gray.shape[0]
    # https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d params
    circles = cv.HoughCircles(
        gray,
        cv.HOUGH_GRADIENT,
        dp=8,
        minDist=rows,
        param1=100,
        param2=50,
        minRadius=500,
        maxRadius=0
    )
    
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 3)
    
    
    cv.namedWindow("detected circles", cv.WINDOW_NORMAL)  # allows resizing
    cv.resizeWindow("detected circles", 600, 800)         # set desired size (width, height)
    cv.imshow("detected circles", src)
    cv.waitKey(0)
    
    return 0
# if __name__ == "__main__":
#     main(sys.argv[1:])
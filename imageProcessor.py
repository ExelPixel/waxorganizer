import cv2
import pytesseract
import config as cfg
from matplotlib import pyplot as plt
from textProcessor import getCatalogNum
from circleDetection import main as detectCircle

def loadImage(imageName):
    image_path = f"Input images/{imageName}"
    image = cv2.imread(image_path)
    assert image is not None, "file could not be read, check if it exists in the directory"
    #Adjust image
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grayImage, (3,3),0)
    # _,binary = cv2.threshold(blur,200,255,cv2.THRESH_BINARY_INV)
    alpha = 1.7  # Contrast control
    beta = -50   # Brightness control
    # contrast = cv2.convertScaleAbs(blur, alpha = alpha, beta = beta)
    adjustedImage = deskewLabel(blur)
    
    return adjustedImage

def deskewLabel(image):
    circles = detectCircle(image)
    circle = circles[0][0]
    center = (circle[0], circle[1])
    radius = circle[2]
    #TODO: Make sure the radius does not extend outside the image 
    #Center the image
    x_start = center[0] - radius
    x_end = center[0] + radius
    y_start = center[1] - radius
    y_end = center[1] + radius
    cropped_image = image[y_start:y_end, x_start:x_end]
    #Rotate image
    rotatedImage = rotateImage(cropped_image)
    return rotatedImage

def rotateImage(image):
    originalImg = image
    
    lines = cv2.HoughLines()
    
    if cfg.debugImageRotation:
        plt.imshow(cv2.cvtColor(originalImg, cv2.COLOR_BGR2RGB))
        plt.title("Detected Lines")
        plt.axis("off")
        plt.show()
    
    return image
    

def extractText(image):
    extracted_text = pytesseract.image_to_string(image)
    if cfg.debugOCR: print(f" Extracted Text:\n {extracted_text}")
    return extracted_text

def debuggingImage(image):
    #Potential bug: BGR2RGB can change the image for other methods too
    rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(rgbImg, output_type=pytesseract.Output.DICT)
    n_boxes = len(data['level'])

    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(rgbImg, (x, y), (x + w, y + h), (255, 0, 0), 1)

    plt.figure(figsize=(10, 6))
    plt.imshow(rgbImg)
    plt.title("Image with Text Bounding Boxes")
    plt.axis("off")
    plt.show()

def runImageProcessor(imageName):
    imageGray = loadImage(imageName)
    text = extractText(imageGray)
    catNum = getCatalogNum(text)
    if cfg.debugOCR: debuggingImage(imageGray)
    return catNum

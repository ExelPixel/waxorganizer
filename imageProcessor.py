import cv2
import pytesseract
import config as cfg
from matplotlib import pyplot as plt
from CircleDetection import main as detectCircle
# from imageSkewing import deskew

# cv2.imshow("Debugging", image_gray)
# cv2.resize(image_gray, None, None, fx=2, fy=2, interpolation=INTER_AREA) #experiment with different interpolation
# cv2.waitKey(0)

def loadImage(imageName):
    image_path = f"Input images/{imageName}"
    image = cv2.imread(image_path)
    assert image is not None, "file could not be read, check if it exists in the directory"
    #Adjust image
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    alpha = 1.5  # Contrast control
    beta = -50    # Brightness control
    contrast = cv2.convertScaleAbs(grayImage, alpha = alpha, beta = beta)
    adjustedImage = deskew(contrast)
    
    # cv2.imwrite("Output text/testimg.jpg", adjustedImage)
    return adjustedImage

def deskew(image):
    circles = detectCircle(image)
    print(circles)
    # circle = circles[0]
    # center = (circle[0], circle[1])
    # radius = circle[2]
    # print(center, radius)

    return image

def debuggingImage(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    n_boxes = len(data['level'])

    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    plt.figure(figsize=(10, 6))
    plt.imshow(image)
    plt.title("Image with Text Bounding Boxes")
    plt.axis("off")
    plt.show()

def extractText(image):
    extracted_text = pytesseract.image_to_string(image)
    if cfg.debugOCR: print(f" Extracted Text:\n {extracted_text}")
    return extracted_text

def getCatalogueNum(imageGray):
    text = extractText(imageGray)
    newLines = text.replace(" ", "").split("\n")
    catalogueNumber = None

    for line in newLines:
        hasSpecialChar = False
        hasAlpha = False
        hasNum = False
        for char in line:
            if not char.isalnum(): 
                hasSpecialChar = True
                break
            if char.isalpha(): hasAlpha = True
            if char.isdigit(): hasNum = True
        if (hasAlpha and hasNum and not hasSpecialChar): 
            catalogueNumber = line

    if catalogueNumber == None:
        return None
    else:
        return catalogueNumber
    
def hasSpecialChar():
    pass

def runImageProcessor(imageName):
    imageGray = loadImage(imageName)
    if cfg.debugOCR: debuggingImage(imageGray)
    return getCatalogueNum(imageGray)

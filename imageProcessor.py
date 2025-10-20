import cv2
import pytesseract
import config as cfg
from matplotlib import pyplot as plt
from CircleDetection import main as detectCircle

# cv2.imshow("Debugging", image_gray)
# cv2.resize(image_gray, None, None, fx=2, fy=2, interpolation=INTER_AREA) #experiment with different interpolation
# cv2.waitKey(0)
ignore = None

def loadImage(imageName):
    image_path = f"Input images/{imageName}"
    image = cv2.imread(image_path)
    assert image is not None, "file could not be read, check if it exists in the directory"
    #Adjust image
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grayImage, (3,3),0)
    _,binary = cv2.threshold(blur,200,255,cv2.THRESH_BINARY_INV)
    # alpha = 1.5  # Contrast control
    # beta = -50    # Brightness control
    # contrast = cv2.convertScaleAbs(grayImage, alpha = alpha, beta = beta)
    adjustedImage = deskewLabel(binary)
    
    return adjustedImage

def deskewLabel(image):
    circles = detectCircle(image)
    circle = circles[0][0]
    center = (circle[0], circle[1])
    radius = circle[2]
    #TODO Make sure the radius does not extend outside the image 
    #Center the image
    x_start = center[0] - radius
    x_end = center[0] + radius
    y_start = center[1] - radius
    y_end = center[1] + radius
    cropped_image = image[y_start:y_end, x_start:x_end]
    #Rotate image
    return cropped_image

def extractText(image):
    extracted_text = pytesseract.image_to_string(image)
    if cfg.debugOCR: print(f" Extracted Text:\n {extracted_text}")
    return extracted_text

def getCatalogueNum(image):
    text = extractText(image)
    # newLines = text.replace(" ", "").split("\n")
    newLines = text.split("\n")
    catalogueNumber = None
    file = open("OCR_Ignore.txt")
    ignore = file.read()
    ignoreList = ignore.split(",")

    for line in newLines:
        relevantLine = stripLine(line, ignoreList)
        print(f" Original: {line}, \nProcessed: {relevantLine}")
        hasSpecialChar = False
        hasAlpha = False
        hasNum = False
        for char in relevantLine:
            if not char.isalnum(): 
                hasSpecialChar = True
                break
            if char.isalpha(): hasAlpha = True
            if char.isdigit(): hasNum = True
        if (hasAlpha and hasNum and not hasSpecialChar): 
            catalogueNumber = relevantLine

    if catalogueNumber == None:
        return None
    else:
        return catalogueNumber
    
def hasSpecialChar():
    pass

def stripLine(line, ignoreList):
    for text in ignoreList:
        index = line.find(text)
        if index != -1:
            return line[:index] + line[index + len(text):]
    return line

def debuggingImage(image):
    rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(rgbImg, output_type=pytesseract.Output.DICT)
    n_boxes = len(data['level'])

    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(rgbImg, (x, y), (x + w, y + h), (255, 0, 0), 3)

    plt.figure(figsize=(10, 6))
    plt.imshow(rgbImg)
    plt.title("Image with Text Bounding Boxes")
    plt.axis("off")
    plt.show()

def runImageProcessor(imageName):
    imageGray= loadImage(imageName)
    if cfg.debugOCR: debuggingImage(imageGray)
    return getCatalogueNum(imageGray)

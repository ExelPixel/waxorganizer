import cv2
import pytesseract
from matplotlib import pyplot as plt
from imageSkewing import deskew

# cv2.imshow("Debugging", image_gray)
# cv2.resize(image_gray, None, None, fx=2, fy=2, interpolation=INTER_AREA) #experiment with different interpolation
# cv2.waitKey(0)

def loadImage(imageName):
    image_path = f"Input images/{imageName}"
    image = cv2.imread(image_path)
    assert image is not None, "file could not be read, check if it exists in the directory"
    #Adjust image
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(grayImage, 170, 220, cv2.THRESH_BINARY) #, 170, 220
    # adjustedImage = deskew(im_bw)
    
    cv2.imwrite("Output text/testimg.jpg", im_bw)
    return im_bw

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

def extractText(image, debuggingMode):
    extracted_text = pytesseract.image_to_string(image)
    if debuggingMode: print(f" Extracted Text:\n {extracted_text}")
    return extracted_text

def getCatalogueNum(imageGray, debuggingMode):
    text = extractText(imageGray, debuggingMode)
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
        return "No catalogue number was found"
    else:
        return catalogueNumber
    
def runImageProcessor(imageName, debuggingMode):
    imageGray = loadImage(imageName)
    if debuggingMode: debuggingImage(imageGray)
    return getCatalogueNum(imageGray, debuggingMode)

import cv2
import pytesseract
from matplotlib import pyplot as plt

# cv2.imshow("Debugging", image_gray)
# cv2.resize(image_gray, None, None, fx=2, fy=2, interpolation=INTER_AREA) #experiment with different interpolation
# cv2.waitKey(0)

# Todo: image rotation/image scaling

debuggingMode = True

def loadImage():
    image_path = "Input images/20250922_215001.jpg"
    image = cv2.imread(image_path)
    assert image is not None, "file could not be read, check if it exists in the directory"
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
    return image_gray, image_rgb

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
    if debuggingMode:
        print(f" Extracted Text:\n {extracted_text}")

#Running code
image_gray, image_rgb = loadImage()
if debuggingMode: debuggingImage(image_rgb)
extractText(image_gray)

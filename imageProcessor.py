import cv2
import pytesseract
from matplotlib import pyplot as plt

image_path = "Input images/20250922_215001.jpg"
image = cv2.imread(image_path)
assert image is not None, "file could not be read, check if it exists in the directory"
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

# cv2.imshow("Debugging", image_gray)
# cv2.resize(image_gray, None, None, fx=2, fy=2, interpolation=INTER_AREA) #experiment with different interpolation
# cv2.waitKey(0)

extracted_text = pytesseract.image_to_string(image_rgb)
print(" Extracted Text:\n")
print(extracted_text)

plt.figure(figsize=(6, 6))
plt.imshow(image_gray)
plt.title("Original Image")
plt.axis("off")
plt.show()


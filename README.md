# waxorganizer
An app that takes images of record labels/covers, contacts Discogs database through an API and sorts information like price, artist name and record title in a text file. So far only the latin alphabet is supported.

How to use program:
1. Take pictures of your record labels in a well lit environment, make sure the label doesnt have glare and make sure it is not at an angle.
2. Put the images you want to process in the "Input images" folder.
3. Change the parameters in the "parameters.txt" file to your liking.
4. Run "main.py" and watch as the program retrieves your desired information and neatly puts it in a sorted text file in the "Output text" folder.

Required libraries:

pip install opencv-python
pip install pytesseract
pip install requests requests-oauthlib

Windows:
https://github.com/UB-Mannheim/tesseract/wiki -> Tesseract OCR
Download using installer then add destination to path variable

https://www.geeksforgeeks.org/python/text-detection-and-extraction-using-opencv-and-ocr/

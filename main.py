import os
from imageProcessor import runImageProcessor

#def loadParamsFromFile():

debuggingMode = False

# imageDirectory = os.fsencode("Input images/")

# for file in os.listdir(imageDirectory):
#     filename = os.fsdecode(file)
#     catNum = runImageProcessor(filename, debuggingMode)
#     print(catNum)

# For testing individual cases
catNum = runImageProcessor("20250922_215001.jpg", debuggingMode)
print(catNum)
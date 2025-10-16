import os
from imageProcessor import runImageProcessor

#def loadParamsFromFile():

debuggingMode = False

imageDirectory = os.fsencode("Input images/")

for file in os.listdir(imageDirectory):
    filename = os.fsdecode(file)
    catNum = runImageProcessor(filename, debuggingMode)
    print(catNum)

# For testing individual cases
# catNum = runImageProcessor("eaab6e043690f3001cda3226f7d2801898bb0383f526d626c24f7935827b3249.jpg", debuggingMode)
print(catNum)

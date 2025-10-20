import os
from imageProcessor import runImageProcessor

#def loadParamsFromFile():

imageDirectory = os.fsencode("Input images/")

def runOneFile(fileName):
    # For testing individual cases
    catNum = runImageProcessor("20251018_190742.jpg")
    print(catNum)

def runAllFiles():
    fileCount = 0
    foundCount = 0
    for file in os.listdir(imageDirectory):
        filename = os.fsdecode(file)
        catNum = runImageProcessor(filename)
        if catNum is not None: 
            foundCount += 1
            print(catNum)
        fileCount += 1

    print(f"Found {foundCount} of {fileCount} catalogueNumbers")

runOneFile("20251018_190742.jpg")
# runAllFiles()

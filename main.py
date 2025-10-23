import os
from discogsIntegration import getRecordName
from imageProcessor import runImageProcessor

#def loadParamsFromFile(): TODO: Get parameters from file

imageDirectory = os.fsencode("Input images/")

#TODO: Make the imageProcessor support other filetypes
def runOneFile(fileName):
    catNum = runImageProcessor(fileName)
    print(f"Catalog number(s): {catNum}")
    print(getRecordName(catNum))

def runAllFiles():
    fileCount = 0
    foundCount = 0
    for file in os.listdir(imageDirectory):
        filename = os.fsdecode(file)
        catNum = runImageProcessor(filename)
        if catNum is not None: 
            foundCount += 1
            print(f"Catalog number(s): {catNum}")
        fileCount += 1

    print(f"Found {foundCount} of {fileCount} catalogNumbers")

runOneFile("1000025947.jpg")
# runAllFiles()

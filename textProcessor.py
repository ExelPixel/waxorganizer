import config as cfg

def getCatalogNum(text):
    newLines = text.split("\n")
    catalogNumber = []
    file = open("OCR_Ignore.txt")
    ignore = file.read()
    ignoreList = ignore.split(",")

    for line in newLines:
        relevantLine = stripLine(line, ignoreList)
        if cfg.debugOCR: print(f" Original: {line}, \nProcessed: {relevantLine}")
        hasAlpha = False
        hasNum = False

        for c in relevantLine:
            if c.isalpha(): hasAlpha = True
            if c.isdigit(): hasNum = True
        if hasAlpha and hasNum: 
            catalogNumber.append(relevantLine)

        #TODO: Sort the list so that the catalog numbers with letters first get priority
        #Optionally accept the following order of letters/numbers: 
        #(letters, numbers) (numbers, letters, numbers) (letters, numbers, letters)?

        #Optionally: Remove all strings that have overlapping elements?
        #Example: Catalog number(s): ['VISIONCAPPEL', 'VISIONANGELS', 'REMIX600', 'ORICINALVERS', 'ONCDCASSETTE']
        catalogNumber.sort()
        newCatNumList = []
        #Shortens the caralogue numbers to 12 characters/numbers
        for catNum in catalogNumber: 
            #Move this check somewhere else?
            slice = catNum[:12]
            #Check that the string doesnt purely consist of numbers?
            if not slice.isalpha(): 
                newCatNumList.append(slice)

    if catalogNumber == []:
        return None
    else:
        return newCatNumList

def stripLine(line, ignoreList):
    newLine = removeSpecialChars(line)
    newLine = removeSingleSymbol(newLine)
    newLine = removeIgnoredSymbols(newLine, ignoreList)
    newLine = newLine.replace(" ", "")
    return newLine

def removeSpecialChars(line):
    newLine = ""
    for c in line:
        #Maybe accept "." too?
        if (c.isalpha() and c.isupper()) or c.isdigit() or c == "-" or c == " ": 
            newLine += c
    return newLine

def removeSingleSymbol(line):
    newLine = ""
    if len(line) > 1:
        lastIndex = len(line)-1
        for i in range(len(line)):
            if i != 0: left = line[i-1]
            elif i == 0: left = None
            if i != lastIndex: right = line[i+1]
            elif i == lastIndex: right = None

            if left == " " and right == " ":
                continue
            elif left == None and right == " ":
                continue
            elif left == " " and right == None:
                continue
            else:
                newLine += line[i]
    else:
        return line
    return newLine

def removeIgnoredSymbols(line, ignoreList):
    for text in ignoreList:
        index = line.find(text)
        if (index != -1 and line[index - 1] == " "): #TODO Check space after too
            line = line[:index] + line[index + len(text):]
    return line

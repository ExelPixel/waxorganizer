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
        if relevantLine == None: continue

        hasAlpha = False
        hasNum = False

        for c in relevantLine:
            if c.isalpha(): hasAlpha = True
            if c.isdigit(): hasNum = True
        if hasAlpha and hasNum: 
            catalogNumber.append(relevantLine)

        newCatNumList = []
        #TODO: Sort the list so that the catalog numbers with letters first get priority
        #Optionally accept the following order of letters/numbers: 
        #(letters, numbers) (numbers, letters, numbers) (letters, numbers, letters)?
        
        for catNum in catalogNumber: 
            slice = catNum[:12]
            if not (slice.isalpha() or slice.isdigit()): 
                newCatNumList.append(slice)

        newCatNumList.sort(reverse=True)

    if catalogNumber == []:
        return None
    else:
        return newCatNumList

def stripLine(line, ignoreList):
    #Play around with the order in which these functions execute
    # line = removeYear(line)
    line = removeSongNames(line)
    if line == None: return None
    line = removeIgnoredSymbols(line, ignoreList)
    line = removeSpecialChars(line)
    line = removeSingleSymbol(line)
    line = line.replace(" ", "")

    if not (line.isalpha() or line.isdigit()): 
        return line
    else:
        return None
    
# def removeYear(line):
#     newLine = ""
#     for i in range(len(line)-3):
#         if line[i:i+3].isdigit():
#             continue
#         else:
#             newLine += line[i]
#     return newLine

def removeSongNames(line):
    for i in range(len(line)):
        lastIndex = len(line)-1
        if i != 0: left = line[i-1]
        elif i == 0: left = ""
        if i != lastIndex: right = line[i+1]
        elif i == lastIndex: right = ""

        if left.isdigit() and line[i] == ":" and right.isdigit():
            return None
    return line
    
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
        if index != -1:
            line = line[:index] + line[index + len(text):]
    return line

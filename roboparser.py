# Timothy Buesking
# Section A
# Homework 3
# CS 3500 Programming Languages and Translators

import sys

relationList = ["<",">","=","#"]
addList = ["+","-","or"]
mulList = ["*","/","and"]
keyWordList = ["=","+","-","*","/","or","and","~","(",")","<",">","=","!","forward","rotate","if","endif","else","while","endw","prog","blip","blorp"]

currToken = ""
currLine = []
currPos = 0
errorFlag = False

def getToken():
    global currToken
    global currLine
    global currPos

    if len(currLine) <= currPos:
        line = sys.stdin.readline()
        currLine = line.strip().split(' ')
        currPos = 0

    currToken = currLine[currPos]
    currPos += 1

def isExpression():
    global errorFlag
    if isSimpleExpression():
        if currToken in relationList:
            getToken()
            if isSimpleExpression():
                return  True
            else:
                errorFlag = True
                return False
        else:
            return True
    else:
        return False

def isSimpleExpression():
    global errorFlag
    if isTerm():
        getToken()
        while(currToken in addList):
            getToken()
            if not isTerm():
                return False

        return True
    return False


def isTerm():
    if isFactor():
        getToken()
        while( currToken in mulList):
            getToken()
            if not isFactor():
                return False
            getToken()
        return True
    else:
        return False


def isFactor():
    global errorFlag

    if isIdentifier():
        return True
    elif isInteger():
        return True
    elif isDecimal():
        return True
    elif currToken == "~":
        return  isFactor()
    elif currToken == "(":
        getToken()
        if isExpression():
            getToken()
            if currToken == ")":
                return True
        errorFlag = True
        return False
    else:
        errorFlag = True
        return False

def isInteger():
    try:
        success = int(currToken)
        return True

    except ValueError:
        return False

def isDecimal():
    try:
        success = float(currToken)
        return True

    except ValueError:
        return False


def isIdentifier():
    global currToken
    if currToken not in keyWordList and currToken[0].isalpha() and currToken.isalnum():
        return True
    else: return False

def isAssignment():
    global errorFlag
    if isIdentifier():
        getToken()
        if currToken == "is":
            if isExpression():
                if currToken == "!":
                    return True
    return False


def isFwdStatement():
    global errorFlag
    getToken()
    if currToken == "(":
        if isExpression():
            getToken()
            if currToken == ")":
                getToken()
                if currToken == "!":
                    return True
    return False


def isRotStatement():
    global errorFlag
    getToken()
    if currToken == "(":
        if isExpression():
            getToken()
            if currToken == ")":
                getToken()
                if currToken == "!":
                    return True
    return False



def isIfStatement():
    global  errorFlag

    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            getToken()
            if currToken == ")":
                if isStatementSequence():
                    getToken()
                    if currToken == "[":
                        getToken()
                        if currToken == "else":
                            if isStatementSequence():
                                getToken()
                                if currToken == "]":
                                    getToken()
                    if currToken == "endif":
                        return True
    return False


def isLoopStatement():
    global errorFlag

    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            getToken()
            if currToken == ")":
                if isStatementSequence():
                    getToken()
                    if currToken == "endw":
                        return True
    return False


def isStatement():
    getToken()
    if currToken == "if":
        return isIfStatement()
    elif currToken == "token":
        return isLoopStatement()
    elif currToken == "forward":
        return isFwdStatement()
    elif currToken == "rotate":
        return isRotStatement()
    elif isAssignment():
        return True

    else: return False


def isStatementSequence():
    global errorFlag

    if isStatement():
        while (isStatement() and not errorFlag):
            pass
        return True

    else:
        errorFlag = True
        return False

def isRoutineDeclaration():
    global currToken
    global currLine
    global errorFlag

    getToken()

    if currToken == "prog":
        getToken()
        if isIdentifier():
            getToken()
            if currToken == "blip":
                if isStatementSequence():
                    if currToken == "blorp":
                        return  True

    errorFlag = True
def isRoutineSequence():
    global errorFlag
    if isRoutineDeclaration():
        while(isRoutineDeclaration() and not errorFlag):
            pass
        if not errorFlag:
            return True
        else:
            return False

    else:
        return False





if __name__== "__main__":
    result = isRoutineSequence()
    if not errorFlag and not result:
        print("CORRECT")
    else:
        print("INVALID!")


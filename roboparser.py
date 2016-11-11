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
    if isSimpleExpression():
        if currToken in relationList:
            getToken()
            if isSimpleExpression():
                return  True
            else:
                quit()
                return False
        else:
            return True
    else:
        return False

def isSimpleExpression():
    if isTerm():
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
            if currToken == ")":
                return True
        quit()
        return False
    else:
        quit()
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
    if isIdentifier():
        getToken()
        if currToken == "is":
            getToken()
            if isExpression():
                if currToken == "!":
                    return True
    return False


def isFwdStatement():
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            if currToken == ")":
                getToken()
                if currToken == "!":
                    return True
    return False


def isRotStatement():
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            if currToken == ")":
                getToken()
                if currToken == "!":
                    return True
    return False



def isIfStatement():
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
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
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            if currToken == ")":
                if isStatementSequence():
                    if currToken == "endw":
                        return True
    return False


def isStatement():
    getToken()
    if currToken == "if":
        return isIfStatement()
    elif currToken == "while":
        return isLoopStatement()
    elif currToken == "forward":
        return isFwdStatement()
    elif currToken == "rotate":
        return isRotStatement()
    elif isAssignment():
        return True

    else: return False


def isStatementSequence():
    if isStatement():
        while isStatement():
            pass
        return True

    else:
        quit()
        return False

def isRoutineDeclaration():
    global currToken
    global currLine

    getToken()

    if currToken == "prog":
        getToken()
        if isIdentifier():
            getToken()
            if currToken == "blip":
                if isStatementSequence():
                    if currToken == "blorp":
                        return  True


def isRoutineSequence():
    if isRoutineDeclaration():
        while isRoutineDeclaration():
            pass

        return True

    else:
        return False


def quit():
    print("INVALID")
    sys.exit()

if __name__== "__main__":
    result = isRoutineSequence()
    if result:
        print("CORRECT")
    else:
        print("INVALID!")


# Timothy Buesking
# Section A
# Homework 3
# CS 3500 Programming Languages and Translators

import sys

# List of relational operators
relationList = ["<", ">", "=", "#"]
# List of addition operators
addList = ["+", "-", "or"]
# List of mutliplication operators
mulList = ["*", "/", "and"]
# List of keywords
keyWordList = ["=", "+", "-", "*", "/", "or", "and", "~", "(", ")", "<", ">", "=", "!", "forward", "rotate", "if",
               "endif", "else", "while", "endw", "prog", "blip", "blorp"]

currToken = ""
currLine = []
currPos = 0


def getToken():
    """
    Gets the next token and stores in global currToken
    :return:
    """
    global currToken
    global currLine
    global currPos

    if len(currLine) <= currPos:
        line = sys.stdin.readline()
        while line.isspace():
            try:
                line = sys.stdin.readline()
            except EOFError:
                line = ""
                break
        currLine = line.strip().split(' ')
        currPos = 0

    currToken = currLine[currPos]
    currPos += 1


def isExpression():
    """
    Determines if the current token string is an expression
    :return:
    """
    if isSimpleExpression():
        if currToken in relationList:
            getToken()
            if isSimpleExpression():
                return True
            else:
                quit()
                return False
        else:
            return True
    else:
        return False


def isSimpleExpression():
    """
    Determines if the current string is a simple expression
    :return:
    """
    if isTerm():
        while currToken in addList:
            getToken()
            if not isTerm():
                return False

        return True
    return False


def isTerm():
    """
    Determines if the token is a term
    :return:
    """
    if isFactor():
        getToken()
        while currToken in mulList:
            getToken()
            if not isFactor():
                return False
            getToken()
        return True
    else:
        return False


def isFactor():
    """
    Determines if the current token is a factor
    :return:
    """
    if isIdentifier():
        return True
    elif isInteger():
        return True
    elif isDecimal():
        return True
    elif currToken == "~":
        getToken()
        return isFactor()
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
    """
    Tries to cast current token to integer and returns if successful or not
    :return:
    """
    try:
        success = int(currToken)
        return True

    except ValueError:
        return False


def isDecimal():
    """
    Tries to cast curren token to decimal and returns if successful or not
    :return:
    """
    try:
        success = float(currToken)
        return True

    except ValueError:
        return False


def isIdentifier():
    """
    Returns if the token is not an indentifier
    :return:
    """
    global currToken
    if len(currToken) > 0 and currToken not in keyWordList and currToken[0].isalpha() and currToken.isalnum():
        return True
    else:
        return False


def isAssignment():
    """
    Returns if the expression is an assignment expression
    :return:
    """
    if isIdentifier():
        getToken()
        if currToken == "is":
            getToken()
            if isExpression():
                if currToken == "!":
                    return True
        quit()
    return False


def isFwdStatement():
    """
    Returns if the foward expression is correct
    :return:
    """
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            if currToken == ")":
                getToken()
                if currToken == "!":
                    return True
    quit()


def isRotStatement():
    """
        Returns if the rotate expression is correct
        :return:
        """
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            if currToken == ")":
                getToken()
                if currToken == "!":
                    return True
    quit()


def isIfStatement():
    """
        Returns if the if expression is correct
        :return:
        """
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            if currToken == ")":
                if isStatementSequence():
                    if currToken == "else":
                        if not isStatementSequence():
                            quit()
                    if currToken == "endif":
                        return True
                    else:
                        quit()
    quit()


def isLoopStatement():
    """
        Returns if the while expression is correct
        :return:
        """
    getToken()
    if currToken == "(":
        getToken()
        if isExpression():
            if currToken == ")":
                if isStatementSequence():
                    if currToken == "endw":
                        return True
                    else:
                        quit()
    quit()


def isStatement():
    """
        Checks to see if the current token is the statement of a statement and then parses that statement
        :return:
        """
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

    else:
        return False


def isStatementSequence():
    """
    Iterates through all statements returning once iterating through all
    :return:
    """
    if isStatement():
        while isStatement():
            pass
        return True


def isRoutineDeclaration():
    """
    Returns if a valid routine is parsed
    :return:
    """
    global currToken
    global currLine

    getToken()

    if currToken == "prog":
        getToken()
        if isIdentifier():
            getToken()
            if currToken == "blip":
                isStatementSequence()
                if currToken == "blorp":
                    return True
        quit()


def isRoutineSequence():
    """
    Returns if all expressions successfully parse into routine declarations
    :return:
    """
    if isRoutineDeclaration():
        while isRoutineDeclaration():
            pass

        return True

    else:
        return False


def quit():
    """
    Exits the program printing invalid with exit code 0
    :return:
    """
    print("INVALID")
    sys.exit()


if __name__ == "__main__":
    result = isRoutineSequence()
    if result:
        print("CORRECT")
    else:
        print("INVALID!")

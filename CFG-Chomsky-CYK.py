class Variable:
    def __init__(self, name):
        self.rightSide = []
        self.name = name
        self.nullable = False
    def addRightSide(self, newRightSide) : 
        if newRightSide == ("e"):
            self.nullable = True
        if ((newRightSide in self.rightSide) == False): 
            if (len(newRightSide) != 0) :
                self.rightSide.append(newRightSide)
    def removeRightSide(self, oldRightSide) :
        self.rightSide.remove(oldRightSide)


lowVar = ord("A")
highVar = ord("Z")
lowTerm = ord("a")
highTerm = ord("z")
variables = []
variableNames = []
terminals = []
terminalVariableIndexes = []
allNullables = []


def insertNewVariable(newLine) : 
    size  = len(variables)
    newVar = newLine[0]
    if (ord(newVar) < lowVar or ord(newVar) > highVar) or (newLine[1:3] != "->") :
        return False
    repeated = False
    index = 0
    for i in range(size):
        if (newVar == variables[i].name) : 
            repeated = True
            index = i
            break
    if repeated == False :
        variables.append(Variable(newVar))
        variableNames.append(newVar)
        index = size
        size += 1
    RightHand = newLine[3:len(newLine)]
    RightHand = RightHand.split("|")
    for i in range(len(RightHand)) : 
        variables[index].addRightSide(RightHand[i])
        for j in range(len(RightHand[i])) : 
            if (ord(RightHand[i][j]) >= lowTerm and ord(RightHand[i][j]) <= highTerm) : 
                if (RightHand[i][j] in terminals) == False : 
                    terminals.append(RightHand[i][j])
    return True

def setNullables(nullables, nullVars) : 
    newNullables = nullables
    newNullVars = nullVars
    for i in range(len(variables)) : 
        if variables[i].nullable == False : 
            isNull = True
            for j in range(len(variables[i].rightSide)) :
                if j != 0 and isNull == True : 
                    break
                isNull = True
                for k in range(len(variables[i].rightSide[j])) : 
                    if ((variables[i].rightSide[j][k] in newNullVars) == False) : 
                        isNull = False
                        break
            if (isNull == True) : 
                variables[i].nullable = True
                newNullVars.append(variables[i].name)
                newNullables += 1
    if (nullables != newNullables) :
        setNullables(newNullables, newNullVars)
    return newNullVars

def deleteNullables(index, varIndex, newRightSide) :
    variables[varIndex].addRightSide(newRightSide)
    if (index >= len(newRightSide)) : 
        return
    for i in range(index,len(newRightSide)) : 
        if (newRightSide[i] in allNullables) :
            deleteNullables(i, varIndex, newRightSide[:i] + newRightSide[i + 1:])
            deleteNullables(i + 1, varIndex, newRightSide)
            break 
    
def isChomsky():
    ans = True
    for i in range(len(variables)):
        if ans == False : 
            break
        for j in range(len(variables[i].rightSide)): 
            if (len(variables[i].rightSide[j]) != 1) and (len(variables[i].rightSide[j]) != 2) : 
                ans = False
                break
            elif (len(variables[i].rightSide[j]) == 1) : 
                if (ord(variables[i].rightSide[j]) < lowTerm) or (ord(variables[i].rightSide[j]) > highTerm)  : 
                    ans = False
                    break
            elif (len(variables[i].rightSide[j]) == 2) : 
                if (ord(variables[i].rightSide[j][0]) < lowVar) or (ord(variables[i].rightSide[j][0]) > highVar)  or (ord(variables[i].rightSide[j][1]) < lowVar) or (ord(variables[i].rightSide[j][1]) > highVar) : 
                    ans = False
                    break
    return ans

def setVariables() : 
    size = len(variables)
    for i in range(len(terminals)) : 
        newVariable = ""
        for j in range(lowVar,highVar + 1) : 
            if (chr(j) in variableNames) == False : 
                newVariable = chr(j)
                break
        variables.append(Variable(newVariable))
        variableNames.append(newVariable)     
        variables[-1].addRightSide(terminals[i])
        terminalVariableIndexes.append(len(variables) - 1)
    for i in range(size) : 
        for j in range(len(variables[i].rightSide)) : 
            for k in range(len(variables[i].rightSide[j])) : 
                if (variables[i].rightSide[j][k] in terminals) : 
                    index = terminals.index(variables[i].rightSide[j][k])
                    variables[i].rightSide[j] = variables[i].rightSide[j][:k] +  variables[terminalVariableIndexes[index]].name + variables[i].rightSide[j][k+1:]
    tempVarsNumber = lowVar
    setChomsky(0, tempVarsNumber)

def setChomsky(i, tempVarNumber):
    if i >= len(variables) : 
        return
    for j in range(len(variables[i].rightSide)) : 
        if len(variables[i].rightSide[j]) > 2 and variables[i].rightSide[j][1] != "(": 
            tempVar = chr(tempVarNumber)
            tempVarNumber += 1
            tempVar = "(V" + tempVar + ")"
            variables.append(Variable(tempVar))
            variableNames.append(tempVar)
            variables[-1].addRightSide(variables[i].rightSide[j][1:])
            variables[i].rightSide[j] = variables[i].rightSide[j][0] + tempVar
            
            setChomsky(i, tempVarNumber)
            break
    setChomsky(i + 1, tempVarNumber)   


while(1):
    newLine = input()
    if newLine == "$" : 
        break
    if (insertNewVariable(newLine) == False) : 
        break
nullables = 0
nullVars = []
for i in range(len(variables)) :
    if variables[i].nullable == True :
        nullables += 1
        nullVars.append(variables[i].name)
nullVars =  setNullables(nullables, nullVars)

allNullables = nullVars
for i in range(len(variables)) : 
    variables[i].rightSide.remove("e") if ("e" in variables[i].rightSide) else 0
    for j in range(len(variables[i].rightSide)) :
        deleteNullables(0, i, variables[i].rightSide[j])
print("nullable variables deleted : ")        
for i in range(len(variables)) : 
    print(variables[i].name, " -> ", variables[i].rightSide)

isChoms = isChomsky()
print(isChoms)
if isChoms == False : 
    setVariables()
print("chomsky form : ")
for i in range(len(variables)) : 
    print(variables[i].name, " -> ", variables[i].rightSide)








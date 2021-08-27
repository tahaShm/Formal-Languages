def getAllClosure (index, preSet, currentSet):
	if preSet == currentSet:
		return currentSet
	else:
		tempCurrent = currentSet
		for i in currentSet.copy():
			currentSet.update(vertexes[i].lambdaClosure)
		return (getAllClosure(index, tempCurrent, currentSet))

def getValidStates (str1, currentSet):
	landa = currentSet
	for i in currentSet.copy():
		landa.update(vertexes[i].lambdaClosure)
	if (len(str1) == 0):
		return landa
	else:
		tempLanda = set()
		for i in landa.copy():
			if (str1[0] == 'a'):
				tempLanda.update(vertexes[i].aout)
			elif (str1[0] == 'b'):
				tempLanda.update(vertexes[i].bout)
			elif (str1[0] == 'c'):
				tempLanda.update(vertexes[i].cout)
			elif (str1[0] == 'd'):
				tempLanda.update(vertexes[i].dout)
		return (getValidStates(str1[1:len(str1)], tempLanda))

class Vertex:
	def __init__(self):
		self.aout = set()
		self.bout = set()
		self.cout = set()
		self.dout = set()
		self.lambdaClosure = set()
	def addOut(self, v, e):
		if e == 'a':
			self.aout.add(v)
		elif e == 'b':
			self.bout.add(v)
		elif e == 'c':
			self.cout.add(v)
		elif e == 'd':
			self.dout.add(v)
		elif e == 'e':
			self.lambdaClosure.add(v)
			
line1 = input()
line1 = line1.split(" ")
n = int(line1[0])
m = int(line1[1])
vertexes = []
paths = [[0 for x in range(3)] for y in range(m)] 
for i in range(n+1):
	vertexes.append(Vertex())
for i in range(m):
	line = input()
	line = line.split(" ")
	paths[i][0] = int(line[0])
	paths[i][1] = int(line[1])
	paths[i][2] = line[2]
for i in range(m):
	vertexes[paths[i][0]].addOut(paths[i][1], paths[i][2])

final = int(input())
finals = set()
line2 = input()
line2 = line2.split(" ")
for i in range(final):
	finals.add(int(line2[i]))
t = int(input())
strings = []
for i in range(t):
	strings.append(input())


for i in range(1,n+1):
	vertexes[i].lambdaClosure = getAllClosure(i, set(), vertexes[i].lambdaClosure)

startState = set()
startState.add(1)

for i in range(t):
	if (strings[i] == "NONE"):
		validStates = vertexes[1].lambdaClosure
	else: 
		validStates = getValidStates(strings[i], startState)

	intersec = validStates.intersection(finals)
	if (len(intersec) == 0) : 
		print("NO")
	elif (len(intersec) > 0) : 
		print("YES")







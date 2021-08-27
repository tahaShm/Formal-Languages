line = input()
temPattern = input()
pattern = '';
for i in range(len(temPattern)):
	if i == 0 or i == len(temPattern) : 
		pattern += temPattern[i]; 
	elif (temPattern[i-1] != temPattern[i] or (temPattern[i-1] == temPattern[i] and temPattern[i] != "*")):
		pattern += temPattern[i]
def checkConformity(line, pattern):
	lineLen = len(line)
	patternLen = len(pattern)
	if len(line) == 0 and len(pattern) == 0:
		return True

	elif len(pattern) == 0 and len(line) > 0:
		return False

	elif len(pattern) > 0 and len(line) == 0:
		if pattern[0] == '*':
			return checkConformity(line, pattern[1:patternLen])
		else:
			return False

	elif line[0] == pattern[0] or pattern[0] == '?':
		return checkConformity(line[1:lineLen], pattern[1:patternLen])

	elif pattern[0] == '*':
		starChecked = False
		for i in range(0,lineLen+1):
			if checkConformity(line[i:lineLen], pattern[1:patternLen]):
				starChecked = True
				break
		if starChecked : 
			return True
		else:
			return False

	else:
		return False
if checkConformity(line, pattern) == True :
	print("YES")
else:
	print("NO")

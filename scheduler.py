availableSlots = [1,2,3,4,5]
individualSlots = [[1],\
					[2], \
					[2], \
					[1], \
					[3]
					] #slots they can make it, [ [A's avail], [B's avail], ... ] 
priorityList = [2,4] #the "must see" guys

# ======= worst case? ========
# availableSlots = []
# individualSlots = []
# numPeople = 33
# for i in range(1,numPeople):
# 	availableSlots.append(i)
# 	indivSlot = []
# 	for j in range(i,numPeople):
# 		indivSlot.insert(0,j)
# 	individualSlots.append(indivSlot)
# ===========================
		
def allocate_helper(ava, indiv): #returns a list of [A's assigned slot, B's assigned slot, ...]
							#returns None if not possible
	if len(indiv) == 0:
		return []
	for i in indiv[0]:
		if i in ava:
			newAva = [j for j in ava if j!=i]
			ret = allocate_helper(newAva, indiv[1:])
			if ret != None:
				ret.insert(0,i)
				return ret
	return None
	
def generateBitmask(n, x): #choose n bits in x bits (<xCn> elements)
	if n == 0:
		return ["0"*x]
	if n == x:
		return ["1"*x]
	if x == 0:
		return []
	
	ret = []
	for i in generateBitmask(n, x-1):
		ret.append("0"+i)
	for i in generateBitmask(n-1, x-1):
		ret.append("1"+i)
	return ret
	
def filterBitmask(priority, bitmask):
	ret = []
	for i in range(len(bitmask)):
		add = True
		for j in range(len(bitmask[i])):
			if bitmask[i][j] != "1":
				continue
			if j+1 in priority:
				add = False
				break;
		if add:
			ret.append(bitmask[i])
	return ret;
		
			
def allocate(ava, indiv, priority): #sorts to increase efficiency (from O(n!) to unknown?)
	ava.sort()
	for i in indiv:
		i.sort()
	
	ret = allocate_helper(ava, indiv)
	
	# removes people who are not in priority list until can,
	# while trying to minimize the number of people removed
	
	i = 0
	while ret == None and i<len(indiv):
		i += 1
		bitmask = filterBitmask(priority, generateBitmask(i, len(indiv)))
		for j in bitmask:
			newIndiv = [indiv[k] for k in range(len(j)) if j[k] == '0']
			ret = allocate_helper(ava, newIndiv)
			if ret != None:
				for k in range(len(j)):
					if j[k] == '1':
						ret.insert(k, -1)
				return ret;
	
	return ret;
	
print(allocate(availableSlots, individualSlots, priorityList))
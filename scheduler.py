availableSlots = [1,2,3,4,5]
individualSlots = [[1,2,3,4,5],\
					[1,2], \
					[1] \
					] #slots they can make it, [ [A's avail], [B's avail], ... ] 
					

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
			
def allocate(ava, indiv): #sorts to increase efficiency (from O(n!) to unknown?)
	ava.sort()
	for i in indiv:
		i.sort()
	indiv.sort(key = lambda x: len(x), reverse = True)
	return allocate_helper(ava, indiv);
			
print(allocate(availableSlots, individualSlots))
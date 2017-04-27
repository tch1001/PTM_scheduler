#  ======= worst case? ========
# availableSlots = []
# individualSlots = []
# numPeople = 33
# for i in range(1,numPeople):
# 	availableSlots.append(i)
# 	indivSlot = []
# 	for j in range(i, numPeople):
# 		indivSlot.insert(0,j)
# 	individualSlots.append(indivSlot)
# print(individualSlots)
#  ===========================
		
def allocate_helper(ava, indiv): # returns a list of [A's assigned slot, B's assigned slot, ...]
							# returns None if not possible
	if len(indiv) == 0: # if no people needed to allocate
		return [] #  return blank allocation
	for i in indiv[0]: # go through first guy's available slots
		if i in ava: # if any is in the available slots
			newAva = [j for j in ava if j!=i] # remove that slot he goes to
			ret = allocate_helper(newAva, indiv[1:]) # continue this with remaining guys and slots
			if ret != None: # if everybody later on can make it
				ret.insert(0,i) # insert this guy in front
				return ret # yay
	return None # if first guy cannot make it to any, whole allocation failed (somenone can't make it)
	
def generateBitmask(n, x): # generates all possible N "on" bits in X bits (<xCn> elements)
	if n == 0: # no need set any?
		return ["0"*x] # return blanks
	if n == x: # need set all?
		return ["1"*x] # return all full
	if x == 0: # no available space
		return [] # return nothing
	
	ret = [] 
	for i in generateBitmask(n, x-1):
		ret.append("0"+i) # choose to set first bit
	for i in generateBitmask(n-1, x-1):
		ret.append("1"+i) # choose to set second bit
	return ret
	
def filterBitmask(priority, bitmask): # gets rid of all bitmasks with Nth bit on
					#  where N is one of the numbers in the Must-Make-It list
	ret = []
	for i in range(len(bitmask)): # goes through all bitmasks
		add = True
		for j in range(len(bitmask[i])): # goes through each bit in the bitmask
			if bitmask[i][j] != "1": # if the bit is indicative of "don't remove"
				continue # dont need check (it's placed like this instead of an "and" operator to save a little runtime)
			if j+1 in priority: # if that bit is indicative of "remove" but cannot remove
				add = False # bye bitmask
				break;
		if add: # if can add
			ret.append(bitmask[i]) # add to filtered bitmasks
	return ret;

			
def allocate(ava, indiv, priority):

	priority.sort()
	ava.sort()
	for i in indiv:
		i.sort()  # sorts to increase efficiency (from O(n!) to unknown?)
		
	ret = allocate_helper(ava, indiv) # first attempt, no change to people
	
	#  if impossible, 
	#  removes people who are not in priority list until can,
	#  while trying to minimize the number of people removed
	
	i = 0
	while ret == None and i<len(indiv): # just keep running till allocation works
		i += 1
		# generate bitmasks of I bits being "on"
		bitmask = filterBitmask(priority, generateBitmask(i, len(indiv)))
		for j in bitmask: # for each bitmask
			newIndiv = [indiv[k] for k in range(len(j)) if j[k] == '0'] # take those "remove" ones out
			ret = allocate_helper(ava, newIndiv) # try to allocate with the changed
			if ret != None: # if success!?
				for k in range(len(j)): # loop through bitmask
					if j[k] == '1': 
						ret.insert(k, -1) # place -1 in positions that were removed
				return ret; # yay
	
	if ret == None: #if priority list, one of them cannot make it
		return allocate(ava, indiv, []) #dont care about the priority list alr

	return ret
	
	
#  ==== documentation ====
#  allocate(availableSlots, individualsCanMakeItSlots, MustSeeList):
#  
#  	returns a list of assigned slots
#  	with -1 being no assigned slot (because of limited space)
#  	e.g. [3, 2, 1, -1, 4]
#  	means the 1st guy got slot 3
#  	2nd guy got slot 2
#  	3rd guy got slot 1
#  	4th guy got no slot
#  	5th guy got slot 4
#   
#   Elimination:
# 	=============	
#	If not everyone's slots are satisfied, 
#	people are removed starting from the latest submission (last in the list),
#	excluding people from the must-make-it list
#
#   if all the people in the must-make-it list still cannot be satisfied, some in the must-make-it list would have
#   no choice but to forfeit going (not given a slot)
#  =======================

availableSlots = [1,2,3,4,5] # possible slots
individualSlots = [[1],\
					[3], \
					[2], \
					[3], \
					[1]
					] #    slots they can make it, 
						#  [ [A's slots], [B's slots], ... ] 
priorityList = [1,3,5] # the must-see guys

print(allocate(availableSlots, individualSlots, priorityList))
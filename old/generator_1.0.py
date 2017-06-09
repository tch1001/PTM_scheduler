import random
from random import shuffle

def randomList(start, end, exclude, d):
	apnd = []
	counter = start
	while(True):
		counter += 1+int(random.random()*(end/d))
		if counter > end:
			break
		if counter != exclude:
			apnd.append(counter)
	return apnd
	
def allCanMakeIt(n):
	ret = []
	for i in range(1, n+1):
		ret.append([i])
		apnd = randomList(1, n, i, 4)
		ret[i-1].extend(apnd)
# 	shuffle(ret)
	return ret

def someCanMakeIt(n):
	ret = []
	for i in range(1, n+1):
		if random.random()>0.9:
			ret.append([i])
			apnd = randomList(1,n,i, 4)
			ret[i-1].extend(apnd)
		else:
			apnd = randomList(1,n,-1, 0.8)
			ret.append(apnd)
# 	shuffle(ret)
	return ret
	
def noneCanMakeIt(n):
	ret = []
	for i in range(1,n+1):
		ret.append([])
		ret[i-1].extend(randomList(int(n/2), int(n), -1, 0.4))
	return ret
	
if __name__ == "__main__":
	print(allCanMakeIt(30))
	print(someCanMakeIt(30))
	print(noneCanMakeIt(30))

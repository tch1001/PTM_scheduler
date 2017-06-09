import csv
import random

outputFile = open("dummydata.csv", 'w', newline='')
outputWriter = csv.writer(outputFile)

outputWriter.writerow(["username", "teacher", "date", "availability"])


alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
TF = ["True", "False"]
teacher = ["Mr Wu", "Dr Lim", "Dr Ong"]
for i in range(32):
	dummylist = []
	a = random.choice(alphabet)
	b = random.choice(alphabet)
	c = random.choice(alphabet)
	d = random.choice(alphabet)
	e = random.randint(0, 9)
	f = random.randint(0, 9)
	g = random.randint(0, 9)
	h = random.choice(alphabet)
	
	mclass = str(random.randint(1,4)) + random.choice(alphabet)

	usr = "21Y" + a + b + c + d + str(e) + str(f) + str(g) + h
	dummylist.append(usr)
	dummylist.append(mclass)
	dummylist.append('date')

	lmao = ""
	for i in range(17):
		lmao += ',' + random.choice(TF)

	lmao = lmao[1:]
	dummylist.append(lmao)

	outputWriter.writerow(dummylist)



outputFile.close()

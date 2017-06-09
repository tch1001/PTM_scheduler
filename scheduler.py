def choose_2withRepetition(n):
    ret = []
    for i in range(n):
        for j in range(i,n):
            ret.append((i,j))
    return ret

temp = ""
indent = 0
gap = 4
def allocate(slots, choices, find = 1, done = []):
    global indent

    if find > len(slots):
        return []

    peopleWithThisSlot = [j for j in choices if find in j[1]]

    choose = choose_2withRepetition(len(peopleWithThisSlot))

    ans = []

    for i in choose:
        if i[0] == i[1]:
            if peopleWithThisSlot[i[0]] in done:
                continue

            done.append(peopleWithThisSlot[i[0]])

            ret = allocate(slots, choices, find+1, done[:])
            ret.append((peopleWithThisSlot[i[0]], find))
            done = done[:-1]


            if len(ret) > len(ans):
                ans = ret
                if len(ans) == len(slots):
                    return ans;


        else:
            if peopleWithThisSlot[i[0]] in done or peopleWithThisSlot[i[1]] in done:
                continue

            done.append(peopleWithThisSlot[i[0]])
            done.append(peopleWithThisSlot[i[1]])

            ret = allocate(slots, choices, find+1, done[:])
            ret.append((peopleWithThisSlot[i[0]], find))
            ret.append((peopleWithThisSlot[i[1]], find))
            done = done[:-2]


            if len(ret) > len(ans):
                ans = ret
                if len(ans) == len(slots):
                    return ans;



    return ans
	

slots = []
choices = []


choices.sort(key = lambda x: len(x))
choices = [(i+1, choices[i]) for i in range(len(choices))]
x = allocate(slots, choices)
print()
print(x)

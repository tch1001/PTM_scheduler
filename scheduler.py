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

    # peopleWithThisSlot = [j for j in choices if find in j[1]]
    # for j in range(len(peopleWithThisSlot)):
    #     if peopleWithThisSlot[j] in done:
    #         continue
    #
    #     done.append(peopleWithThisSlot[j])
    #
    #     ret = allocate(slots[1:], choices, find+1, done)
    #     if ret != None:
    #         print(ret)
    #         ret.append((peopleWithThisSlot[j], find))
    #         if len(ret) > len(ans):
    #             ans = ret
    #
    #     for k in range(j+1,len(peopleWithThisSlot)):
    #         if peopleWithThisSlot[k] in done:
    #             continue
    #         # print(i, ":", peopleWithThisSlot[j], peopleWithThisSlot[k])
    #         # print('meow')
    #         done.append(peopleWithThisSlot[k])
    #         ret = allocate(slots[1:], choices, find+1, done)
    #         if ret != None:
    #             print(ret)
    #             # print('mew')
    #             ret.append((peopleWithThisSlot[k], find))
    #             if len(ret) > len(ans):
    #                 ans = ret
    #         done = done[:-1]
    #     done = done[:-1]
    # return ans
        # print(i,":",peopleWithThisSlot)
	

slots = []
choices = []


choices.sort(key = lambda x: len(x))
choices = [(i+1, choices[i]) for i in range(len(choices))]
x = allocate(slots, choices)
print()
print(x)

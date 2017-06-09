import csv
import sys
import random

# ==========(below) not-so-good algorithms attempted============
def choose_2withRepetition(n):
    ret = []
    for i in range(n):
        for j in range(i,n):
            ret.append((i,j))
    return ret

def allocate(slots, choices, find = 1, done = []):
    if len(done) == len(slots):
        exit()

    if find > len(slots):
        return []

    peopleWithThisSlot = [j for j in choices if find in j[1]]

    choose = choose_2withRepetition(len(peopleWithThisSlot))

    ans = allocate(slots, choices, find+1, done[:])

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

def allocateGreedyNonOptimal(slots, choices):
    places = [0 for i in range(len(slots)+1)]
    ret = []
    for i in choices:
        for j in i[1]:
            if places[j] >= 2:
                continue
            places[j] += 1
            ret.append((j,i))
            break

    ret.sort(key = lambda x: x[0])
    return ret



# =========(above) not-so-good algorithms attempted=============






# =========(below) working algorithms ==========================

def allocateGreedy(slots, choices, places = None):
    if len(choices) == 0:
        return []
    if places == None:
        places = [0 for i in range(len(slots)+1)]
    ret = []
    for j in choices[0][1]:
        if places[j]>=2:
            continue
        places[j] += 1
        recurse = allocateGreedy(slots, choices[1:], places[:])
        if recurse != None:
            ret.append((j, choices[0]))
            ret.extend(recurse)
            ret.sort(key = lambda x: x[0])
            return ret
        # oh no, it returns None, that means there is no good allocation
        places[j] -= 1;
        recurse = allocateGreedy(slots, choices[1:], places[:])
        return recurse
    return None


def readCSV(name):
    file = open(name)
    fileReader = csv.reader(file)
    rawData = list(fileReader)

    slots = [i+1 for i in range(18)]
    choices = []
    for i in rawData:
        if 'username' in i:
            continue

        availability = i[3].split(',')
        choices.append([j+1 for j in range(len(availability)) if availability[j].lower() == 'true'])

    return slots, choices

if __name__ == "__main__":
    slots = []
    choices = []

    filename = sys.argv[1]
    slots, choices = readCSV(filename)

    choices.sort()
    choices.sort(key = lambda x: len(x))
    choices = [(i+1, choices[i]) for i in range(len(choices))]


    x = allocateGreedy(slots, choices)
    # the above uses bruteforce but in a greedy manner
    # this greedy algorithm loops through every person,
    # and directly attempts to assign him a slot which he has in hsi availability list
    # It does not guarantee the "best" solution, (some people might not get a slot)
    # but runs in O(nm)
    # where n is the number of people and m is the number of slots

    # y = allocateGreedyNonOptimal(slots, choices)



    # x = allocate(slots, choices)
    # the above uses bruteforce recursive backtracking,
    # but takes too long with more than 7 people
    # as it runs in exponential time (by visiting every single possibility)

    for i in x:
        assert i[0] in i[1][1]


    print(x)

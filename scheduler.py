import csv
import sys
import random

# ==========(below) not-so-good algorithms attempted============
def choose_2withRepetition(n): #choose a pair of indices from n indices
                                # e.g choose_2withRepetition(4) would return
    # [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
    # there are no repeated pairs (a,b) and (b,a)
    # but there can be pairs of repeated indices (a,a)
    ret = []
    for i in range(n): #first index from 0 to n-1
        for j in range(i,n): #second index from first index to n-1
            ret.append((i,j)) #add to the list
    return ret #return the list

def allocate(slots, choices, find = 1, done = []): #recursive function
                     # takes in slots, choices, the slot to find people to occupy (find),
                     # and the people who already have a slot (done)

    if find > len(slots): #if we are trying to find something out of range
        return [] #return

    # find the people with this slot <find> in their availability list
    peopleWithThisSlot = [j for j in choices if find in j[1]]

    # case 1: no one selects slot <find>
    ans = allocate(slots, choices, find+1, done[:])


    # case 2 and 3: one or two people select slot <find>

    choose = choose_2withRepetition(len(peopleWithThisSlot))
    # find the possible ways to choose them (generate possible pairs)
    # note: includes (a,a), which signifies that there is one person choosing this slot

    # for all pairs (some are 'same-person-pair' ((a,a)), while others are (a,b))
    for i in choose:
        if i[0] == i[1]: # if it is the form of (a,a)
            if peopleWithThisSlot[i[0]] in done: #c heck if this person has been given already
                continue # if so, skip this guy

            done.append(peopleWithThisSlot[i[0]]) # if not, add him to the "given a slot" list

            ret = allocate(slots, choices, find+1, done[:]) #r ecurse
                    # also, done[:] is used as we do not want to pass in the reference to the object
                    # but instead want to pass in a copy of this object
                    # (was a huge source of bug previously)
            ret.append((peopleWithThisSlot[i[0]], find)) #add this guy and his slot to the 'answer'


            if len(ret) > len(ans): # if this results in a better solution
                ans = ret # replace the old solution
                if len(ans) == len(slots): # if this solution is 'perfect',
                                        # that means, everyone is given a slot
                    return ans; #we have found the ideal solution!!

            done = done[:-1] #remove this guy for the other recursions


        else: # two people having slot <find> instead of one
            if peopleWithThisSlot[i[0]] in done or peopleWithThisSlot[i[1]] in done: #if either one is given a slot already
                continue # skip this pair of people

            done.append(peopleWithThisSlot[i[0]]) # add these two people
            done.append(peopleWithThisSlot[i[1]]) # to the 'given a slot' list

            ret = allocate(slots, choices, find+1, done[:]) # recurse
            ret.append((peopleWithThisSlot[i[0]], find)) # add these two people
            ret.append((peopleWithThisSlot[i[1]], find)) # to the solution


            if len(ret) > len(ans): # if this is a better answer than the existing answer
                ans = ret # replace the old answer
                if len(ans) == len(slots): # if this answer is 'perfect'
                    return ans; # yay return it

            done = done[:-2] # remove these two people from the 'given a slot' list



    return ans # return the answer (which is maxed out)


# after realising the above bruteforce takes too long
def allocateGreedyNonOptimal(slots, choices):  # a better answer
    places = [0 for i in range(len(slots)+1)] # create a list "places"
                        # to represent the number of people per slot
                        # where place[n] == number of people in slot n
    ret = [] # init a blank return solution
    for i in choices: # in each individual's availability (<id>, [<slots>])
        for j in i[1]: # loop through his slots (strictly increasing)
            if places[j] >= 2: # if that slot is full/taken by two peole
                continue # skip it
            ret.append((j,i)) # else we can add this guy to that slot
            places[j] += 1 # and update the counter for the people in that slot
            break # stop and don't let this guy take multiple slots

    ret.sort(key = lambda x: x[0]) # sort according to the slot given to people
    return ret # return
# =========(above) not-so-good algorithms attempted=============







# =========(below) working algorithms ==========================

def allocateGreedy(slots, choices, places = None): # recursive greedy function
    if len(choices) == 0: # if there are no more people to allocate
        return [] # return a blank
    if places == None: # (only the first call)
        places = [0 for i in range(len(slots)+1)]
        # we init place, where places[n] == number of people taking slot n,
        # to be zero for everything
    ret = [] # init a blank return value
    for j in choices[0][1]: # choices[0][1] is the 1st person's available slots
                    # we loop through his available slots
        if places[j]>=2: # if that slot is taken by 2 people
            continue # skip that slot
        places[j] += 1 # add the counter (this guy is taking this slot)
        recurse = allocateGreedy(slots, choices[1:], places[:]) # recurse for the next guy
                                        # and also, we used places[:] to copy the array
                                        # instead of pass its reference
        if recurse != None: # if we did not fail to allocate the others
            ret.append((j, choices[0])) # add this guy to the slot
            ret.extend(recurse) # add the rest of the answers
            ret.sort(key = lambda x: x[0]) # sort it for neatness (according to the slot number_
            return ret # and return it
        # oh no, recursion returns None, that means there is no good allocation
        places[j] -= 1; # free one place for this slot
        recurse = allocateGreedy(slots, choices[1:], places[:])
                    # recurse, but we do not add this guy to his slot
                    # meaning that someone later on can take his slot
                    # this (poor) guy does not have any slots
        return recurse # return the answer
    return None


def readCSV(name): # a function to read from a csv and return slots and people's availabilities
    file = open(name) # open the file
    fileReader = csv.reader(file) # get the csv reader object
    rawData = list(fileReader) # convert it to a list

    slots = [i+1 for i in range(18)] # slots are hardcoded in (17 slots)
    choices = [] # choices init to be blank
    for i in rawData: # for each row
        if 'username' in i: # if it is the title/heading
            continue # skip the row

        # i[0] is the username
        # i[1] is the class
        # i[2] is the timestamp
        # i[3] is the availability in the form of "True,False,False,True..."
        availability = i[3].split(',') # make the availability an array
        choices.append([j+1 for j in range(len(availability)) if availability[j].lower() == 'true'])
        # if the i-th index is 'True', it is part of the list generated by the list comprehension

    file.close() # close the file
    return slots, choices # return slots and choices

if __name__ == "__main__":

    filename = sys.argv[1] # get the filename parameter
    slots, choices = readCSV(filename) # read the csv

    choices.sort() # sort the choices (according to alphanumeric) ([1,2,3] comes before [2,3,4]
    choices.sort(key = lambda x: len(x)) # sort them according to length
    choices = [(i+1, choices[i]) for i in range(len(choices))] # label each one (1-indexed)


    x = allocateGreedy(slots, choices) # allocate!
    # the above uses bruteforce but in a greedy manner
    # this greedy algorithm loops through every person,
    # and directly attempts to assign him a slot which he has in hsi availability list
    # It does not guarantee the "best" solution, (some people might not get a slot)
    # but runs in O(nm)
    # where n is the number of people and m is the number of slots



    # x = allocateGreedyNonOptimal(slots, choices)
    # similar to allocateGreedy(), but this might not give the 'perfect' solution


    # x = allocate(slots, choices)
    # the above uses bruteforce recursive backtracking,
    # but takes too long with more than 7 people
    # as it runs in exponential time (by visiting every single possibility)

    for i in x:
        assert i[0] in i[1][1] # just double check if each person's allocation is in his availability list


    print(x) # print the results
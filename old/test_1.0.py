import scheduler
import generator

slots = 12
people = 10 #starts waiting for really long after 20
ava = [i for i in range(1,slots+1)]
print(scheduler.allocate(ava, generator.allCanMakeIt(people), ava)) #ava as the priority list as well
print(scheduler.allocate(ava, generator.someCanMakeIt(people), ava)) #ava as the priority list as well
print(scheduler.allocate(ava, generator.noneCanMakeIt(people), ava)) #ava as the priority list as well

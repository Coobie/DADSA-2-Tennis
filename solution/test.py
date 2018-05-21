__author__ = "JGC"  # Author: JGC


import cProfile
import extra as ex
import random

class Test(object):

    def __init__(self,num):
        self.__number = num

    def get_name(self):
        return str(self.__number)

    def __str__(self):
        return str(self.__number)

def search_linear(list, name):
    for i in range(0,len(list)):
        if list[i].get_name() == name:
            return i
    return None


number = 32  # Size of the list

test_list = []

for i in range(0, number):
    temp_test = Test(str(random.randrange(0,number)))
    test_list.append(temp_test)

temp = []
for i in test_list:
    temp.append(i)
pr = cProfile.Profile()
pr.enable()
temp.sort(key=lambda obj: obj.get_name(), reverse=False)
pr.disable()
pr.print_stats()
print(test_list)
print(temp)
pi = cProfile.Profile()
pi.enable()

pi.disable()
pi.print_stats()

print("%02d"%(100))

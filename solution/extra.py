__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")


def binary_search(list, value):
    """"
    Binary search for an ordered list
    :return int : position (if it is found)
    :return None : not found in list
    """
    lo, hi = 0, len(list) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if list[mid] < value:
            lo = mid + 1
        elif value < list[mid]:
            hi = mid - 1
        else:
            return mid
    return None


def binary_search_class(list, name):
    """"
    Performs binary search on list of class with get_name method (ordered)
    :return int : position (if it is found)
    :return None : not found in list
    """
    lo, hi = 0, len(list) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if list[mid].get_name() < name:
            lo = mid + 1
        elif name < list[mid].get_name():
            hi = mid - 1
        else:
            return mid
    return None


def valid_match(max,a,b):
    """Checks if match is valid (not players in the match)"""
    max = int(max)
    if((a == max or b == max) and (a is not b)):
        return True
    else:
        return False

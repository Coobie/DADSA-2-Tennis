__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")


class Factor(object):
    """Class for a factor"""

    def __init__(self,amount,difference):
        """
        Constructor for factor
        :param float amount: multiplier
        :param int difference: different in points
        """
        self.__amount = amount
        self.__diff = difference

    def get_amount(self):
        """
        Get the amount (multiplier)
        :return float amount: the multiplier for the points
        """
        return self.__amount

    def get_diff(self):
        """
        Get the difference in points required for the factor
        :return int diff: difference in points (w - l)
        """
        return self.__diff
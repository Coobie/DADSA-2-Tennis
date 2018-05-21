__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": #File is opened directly
    print("This file has been called incorrectly")


class Round(object):
    """This is the class for a round"""

    def __init__(self,number,max):
        """
        Constructor for round
        :param int number: the round number
        :param int max: max number of matches in the round
        """
        self.__number = number
        self.__matches = []
        self.__winners = []
        self.__status = 0
        self.__max_number_matches = max

    def get_matches(self):
        """
        Gets the matches in the round
        :return List<Match>: list of matches in the round
        """
        return self.__matches

    def add_match(self,match):
        """
        Adds match to the round
        :param Match match: the match
        :return: void
        """
        self.__matches.append(match)

    def get_number(self):
        """
        Gets the round number
        :return int number: the round number
        """
        return self.__number

    def get_name(self):
        """
        Gets the name of the round
        :return str number: str version of the number
        """
        return self.get_number()

    def get_winners(self):
        """
        Gets list of winners of the round
        :return List<str>: list of winners names
        """
        return self.__winners

    def add_winner(self,player):
        """
        Adds winner's name to list of winners
        :param str player: name of the player that won a match
        :return: void
        """
        self.__winners.append(player)

    def get_max_matches(self):
        """
        Gets the max number of matches that the round can have
        :return int max_number_matches: max number of matches
        """
        return self.__max_number_matches

    def set_status(self,st):
        """
        Sets the status of the round
        :param int st: status
        :return: void
        """
        self.__status = st

    def get_status(self):
        """
        Gets the status of the round
        :return int status: the status of the round
        """
        return self.__status
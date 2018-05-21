__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")


class Track(object):
    """The class for a track"""

    def __init__(self, name, best, pl,factors):
        """
        Constructor for track
        :param str name: name of the track
        :param int best: the number of sets to win a match
        :param str pl: player type
        """
        self.__name = name
        self.__rounds = []
        self.__best_of = best
        self.__player_type = pl
        self.__ranking_factors = factors


    def get_name(self):
        """
        Gets the name of the track
        :return str: name of the track
        """
        return self.__name

    def get_player_type(self):
        """
        Gets the player type
        :return str: the type of the players
        """
        return self.__player_type

    def get_best_of(self):
        """
        Gets the the number of sets to win a match
        :return int : number of sets to win
        """
        return self.__best_of

    def get_factors(self):
        """
        Gets the factors for the track
        :return List<Factor>: the factors
        """
        return self.__ranking_factors

    def get_rounds(self):
        """
        Gets the rounds for the track
        :return List<Round>: the rounds
        """
        return self.__rounds

    def set_rounds(self,rounds):
        """
        Sets the rounds for the track
        :param List<Round> rounds:
        :return: void
        """
        self.__rounds = rounds

    def add_round(self,round):
        """
        Adds a round to the rounds for a track
        :param Round round: the round wanting to add
        :return: void
        """
        self.__rounds.append(round)

    def get_round(self,i):
        """
        Gets the round
        :param int i: the index of the round
        :return Round: the round at position i
        """
        return self.__rounds[i]

    def __str__(self):
        """String representation of track"""
        st = self.__name + " which is best of "+ str(self.get_best_of())
        return st
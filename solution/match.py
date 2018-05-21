__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")

class Match(object):

    def __init__(self,p_a,p_a_s,p_b,p_b_s):
        """
        Constructor for match
        :param str p_a: player a name
        :param int p_a_s: player a points
        :param str p_b: player b name
        :param int p_b_s: player b score
        """
        self.__player_a = p_a
        self.__player_b = p_b
        self.__score_a = p_a_s
        self.__score_b = p_b_s

    def get_player_a(self):
        """
        player a name
        :return str player_a:
        """
        return self.__player_a

    def get_player_b(self):
        """
        player b name
        :return str player_b:
        """
        return self.__player_b

    def get_a_score(self):
        """
        player a score
        :return int score_a: player a score
        """
        return self.__score_a

    def get_b_score(self):
        """
        player b score
        :return int score_b: player b score
        """
        return self.__score_b

    def __str__(self):
        """
        to string for match
        :return str: string representation of a match
        """
        return (self.get_player_a()+" "+str(self.get_a_score())+" "+self.get_player_b()+" "+str(self.get_b_score()))
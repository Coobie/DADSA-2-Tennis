__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")

class Player(object):

    def __init__(self, name, type):
        """
        Constructor for player
        :param str name: player's name
        :param str type: player's type
        """
        self.__name = name
        self.__type = type
        self.__ranking = []
        self.__prize_money = []
        self.__matches = []
        self.__number_tournaments = 0

    def get_name(self):
        """
        Getter for name
        :return str name: player name
        """
        return self.__name

    def get_type(self):
        """
        Getter for type
        :return str type: player type
        """
        return self.__type

    def set_number_tournaments(self, num):
        """
        Setter for number of tournaments
        :param int num:
        :return: void
        """
        self.number_tournaments = num
        for i in range(0, num):
            self.__ranking.append(0.0)
            self.__prize_money.append(0)
            self.__matches.append([])

    def set_rank(self, rank, tourn):
        """
        Sets the rank for a player in a tournament
        :param float rank: the ranking points for the tournament
        :param int tourn: number of the tournament
        :return: void
        """
        self.__ranking[tourn] = round(rank, 2)

    def get_rank(self,tourn):
        """
        Sets the rank for a player in a tournament
        :param int tourn: number of the tournament
        :return: float ranking points
        """
        return self.__ranking[tourn]

    def get_total_ranking(self):
        """
        Adds up all of the ranking points
        :return float output: total number of ranking points
        """
        output = 0
        for i in self.__ranking:
            output += i
        return output

    def set_prize_money(self, prize, tourn):
        """
        Sets the prize money per tournament
        :param float prize: the prize money
        :param int tourn: tournament number/index
        :return: void
        """
        self.__prize_money[tourn] = round(prize, 2)

    def get_prize_money(self,tourn):
        """
        Gets the prize money that the player got in a tournament
        :param int tourn: the tournament number
        :return float prize_money: the prize money the player got in a given tournament
        """
        return self.__prize_money[tourn]

    def get_total_prize_money(self):
        """
        The total prize money for the player
        :return float output: total prize money
        """
        output = 0
        for i in self.__prize_money:
            output += i
        return output

    def get_all_matches(self):
        """
        All of the matches that a player was in
        :return List<List<Match>>: all matches per tournament
        """
        return self.__matches

    def get_matches(self,i):
        """
        Get matches for a tournament
        :param int i: the tournament number
        :return List<Match>: matches that the player was in (in given tournament)
        """
        return self.__matches[i]

    def add_match(self,t,match):
        """
        Adds match to player per tournament
        :param in t: tournament id
        :param Match match: the match
        :return: void
        """
        self.__matches[t].append(match)

    def __str__(self):
        """
        String representation of player
        :return str : player
        """
        return self.get_name()
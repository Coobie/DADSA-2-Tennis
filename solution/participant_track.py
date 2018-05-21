__author__ = "JGC"  # Author: JGC

if __name__ == "__main__": #File is opened directly
    print("This file has been called incorrectly")


class ParticipantTrack(object):
    """This is the class for holding players for a track"""

    def __init__(self,type,name):
        """
        Constructor for ParticipantTrack
        :param str type: the player type
        :param str name: the playe type name
        """
        self.__players = []
        self.__name = name
        self.__type = type

    def add_player(self,player):
        """
        Adds a player to the ParticipantTrack
        :param Player player: the player
        :return: void
        """
        self.__players.append(player)

    def get_players(self):
        """
        Gets players
        :return List<Player>: list of the players
        """
        return self.__players

    def get_player(self,i):
        """
        Gets player at an index
        :param i: index
        :return Player: the player at position i
        """
        return self.__players[i]

    def get_type(self):
        """
        Gets the type of the ParticipantTrack
        :return str type: type of players in ParticipantTrack
        """
        return self.__type

    def get_name(self):
        """
        Gets the name of the ParticipantTrack
        :return str name: name of the ParticipantTrack
        """
        return self.__name

    def number_of_players(self):
        """
        The number of players in the ParticipantTrack
        :return int: the number of players in ParticipantTrack
        """
        return len(self.get_players())
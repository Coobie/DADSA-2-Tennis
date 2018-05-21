__author__ = "JGC"  #Author: JGC

if __name__ == "__main__": # File is opened directly
    print("This file has been called incorrectly")
    
class Tournament(object):

    def __init__(self, name,diff,money_list):
        """
        Constructor for tournament
        :param str name: name of tournament
        :param float diff: difficulty of tournament
        :param List<float> money_list: list of prize money for the tournament
        """
        self.__name = name
        self.__difficulty = diff
        self.__tracks = []
        self.__prize_money = []
        self.set_prize_money(money_list)

    def add_track(self,tk):
        """
        Adds new track to the tournament
        :param track tk: the track you want to add
        :return: void
        """
        self.__tracks.append(tk)

    def set_prize_money(self,list):
        """
        Setter for prize money
        :param List<float> list:
        :return: void
        """
        for i in list:
            self.__prize_money.append(i)

    def get_prize_money(self, i):
        """
        Gets prize money from list
        :param int i: the index in the list of prize money
        :return:
        """
        return self.__prize_money[i]

    def add_prize_money(self,i):
        """
        Adds prize money to list of prize money
        :param float i: the new amount of prize money to add to list
        :return: void
        """
        self.__prize_money.append(i)

    def get_prize_money_all(self):
        """
        Gets the list of prize money
        :return: List<float>
        """
        return self.__prize_money

    def sort_prize_money(self):
        """
        Sorts the list of prize money
        :return: void
        """
        self.__prize_money.sort()

    def get_name(self):
        """
        Getter for name of tournament
        :return str name: name of tournament
        """
        return self.__name

    def get_tracks(self):
        """
        Gets all tracks for a tournament
        :return List<track>: whole list of tracks
        """
        return self.__tracks

    def get_track(self,id):
        """
        Gets one track from list
        :param int id: the index of the track
        :return track: one track from the list
        """
        return self.__tracks[id]

    def number_tracks(self):
        """
        Number of tracks
        :return int: number of tracks
        """
        return len(self.__tracks)

    def get_difficulty(self):
        """
        Gets difficulty of tournament
        :return float: the diff of tournament
        """
        return float(self.__difficulty)

    def __str__(self):
        """String representation of tournament"""
        st = self.__name +" "+ str(self.__difficulty)+"\n      "
        for i in range(len(self.__tracks)):
            st += "- "+str(self.__tracks[i]) + "\n      "
        return st
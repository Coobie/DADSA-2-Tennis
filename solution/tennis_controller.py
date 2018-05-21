__author__ = "JGC"  # Author: JGC

from season import Season
from tournament import Tournament
from track import Track
from player import Player
from match import Match
from round import Round
from factor import Factor
from participant_track import ParticipantTrack
import extra as ex
import os.path
import csv
import math
import cProfile
import pickle
import time

# All files and folders
my_path = os.path.abspath(os.path.dirname(__file__))  # Relative path of files
round_paths = ""
data_paths = ""
output_path = ""
if __name__ == "__main__":  # File is opened directly
    start = True
else:
    start = False

players=[]
seasons=[]

with open("CONFIG.txt") as f:  # Read config file
    for line in f:
        if "DATA" in line:  # Get data path from config
            address_folder = line.split('"')
            data_paths = address_folder[1]
        elif "ROUND" in line:  # Get round path from config
            address_folder = line.split('"')
            round_paths = address_folder[1]
        elif "OUTPUT" in line:  # Get output path from config
            address_folder = line.split('"')
            output_path = address_folder[1]

if (round_paths == "" and data_paths == "" and output_path == ""):
    start = False

def read_settings():
    """This loads in all of the data from the csv files for creating objects"""
    tourn_info = os.path.join(my_path, ".." + data_paths + "TOURNAMENT INFO.csv")
    track_info = os.path.join(my_path, ".." + data_paths + "TRACK INFO.csv")
    ranking_points = os.path.join(my_path, ".." + data_paths + "DADSA 17-18 COURSEWORK B RANKING POINTS.csv")

    ranking_list = []
    with open(ranking_points, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            temp = int(row["Tournament Ranking Points"])
            if temp is not None:
                ranking_list.sort()
                if (ex.binary_search(ranking_list, temp) == None):
                    ranking_list.append(temp)
            ranking_list.sort()
    # Find out the number of columns in the tournament info csv
    number_columns = 0
    with open(tourn_info, 'r') as f1:
        csvlines = csv.reader(f1, delimiter=',')
        for lineNum, line in enumerate(csvlines):
            if lineNum == 0:
                number_columns = (len(line))
                break
            break

    # Find all of the seasons in the file and load them into seasons
    season_list = []
    with open(tourn_info, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            temp = row["Season"]
            if temp is not None:
                if (ex.binary_search(season_list, temp) == None):
                    season_list.append(temp)
    for i in season_list:
        seasons.append(Season(i, ranking_list))

    # Load in all tournaments to their respective seasons
    # Also finds which places get prize money
    for i in seasons:
        with open(tourn_info, 'r') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                if (row["Season"] == i.get_name()):
                    temp = []
                    row_name = "Place "
                    number_places = (number_columns - 3)
                    for x in range(0, number_places):
                        temp.append(float(row[row_name + str(x + 1)].replace(',', '')))
                    new_list = list(set(temp))  # Find unique elements in list
                    i.add_tournament(Tournament(row["Tournament"], row["Difficulty"], new_list))

    # Load in tracks for each tournament
    for x in seasons:
        for j in x.get_tournaments():
            with open(track_info, 'r') as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    if (row["Season"] == x.get_name()) and (row["Tournament"] == j.get_name()):
                        factors = [Factor(float(row["Factor1Amount"]),int(row["Factor1Diff"])),Factor(float(row["Factor2Amount"]),int(row["Factor2Diff"]))]
                        j.add_track(Track(row["Track"], row["Best Of"], row["Players"],factors))

    # Add players to seasons
    list_all_tracks = []
    for s in seasons:
        for t in s.get_tournaments():
            track_num = 0
            for k in t.get_tracks():
                if (ex.binary_search(list_all_tracks, k.get_player_type()) == None):
                    list_all_tracks.append(k.get_player_type())
                    list_all_tracks.sort()
                    pt = ParticipantTrack(k.get_player_type(),k.get_name())
                    with open(os.path.join(my_path, ".."+data_paths+"DADSA 17-18 COURSEWORK B "+k.get_player_type()+" PlAYERS.csv"), 'r') as csvFile:
                        reader = csv.DictReader(csvFile)
                        for row in reader:
                            player = Player(row["Player"],k.get_player_type())
                            player.set_number_tournaments(s.number_tournaments())
                            pt.add_player(player)
                    s.add_participants(pt)
                    players.append(pt)
                number_rounds = int(math.log2(pt.number_of_players()))
                temp_number_matches = pt.number_of_players()
                for i in range(0,int(number_rounds)):
                    k.add_round(Round(str(i+1),int(temp_number_matches/2)))
                    temp_number_matches = temp_number_matches / 2

    # Set starting point
    seasons[0].get_tournament(0).get_track(0).get_round(0).set_status(1)
    seasons[0].get_tournament(0).get_track(1).get_round(0).set_status(1)


def user_prompted_match(max,match):
    """
    This is what pops up to the user if a match is either wrong in the csv files or manual input is wrong
    :param int max: the max number of points
    :param Match match: valid match
    :return:
    """
    print("The system has detected that the following match is incorrect:")
    print(match)
    print("Please enter the result again")
    print("PlayerA ScoreA PlayerB ScoreB")
    match_input = input("Enter the match in the format above: ")
    match_input = match_input.split(" ")  # Split the input into list that should be 4 length
    if len(match_input) == 4:
        if match_input[0] == match.get_player_a() and match_input[2] == match.get_player_b():
            if match_input[1].isdigit() and match_input[3].isdigit():
                # both values are digits
                return Match(match.get_player_a(), int(match_input[1]), match.get_player_b(),int(match_input[3]))
            elif match_input[1] == "i" and match_input[3].isdigit() and int(match_input[3]) is not max:
                # first player is injured
                return Match(match.get_player_a(),int(max)-1,match.get_player_b(),int(max))
            elif match_input[1].isdigit() and match_input[3] == "i" and int(match_input[1]) is not max:
                # first player is injured
                return Match(match.get_player_a(),int(max),match.get_player_b(),int(max)-1)
        else:
            print("Incorrect players")
    else:
        print("Incorrect format")
    return match


def match_check(max,match):
    """
    Checks that the scores are valid for a match
    :param int max: the max number of points in a match
    :param Match match: the match in question
    :return Match match: the correct match
    """
    a_score = match.get_a_score()
    b_score = match.get_b_score()

    max = int(max)
    if ((a_score == max or b_score == max) and a_score is not b_score):
        # Match is valid
        return match
    else:
        return match_check(max,user_prompted_match(max,match))


def match_check_players(s,t,tk,r,match):
    """
    Checks if players are allowed to play in that round of the tournament
    :param int s: season id
    :param int t: tournament id
    :param int tk: track id
    :param int r: round id
    :param Match match: the match to check
    :return int 1: players can play against each other in this round
    :return int 2: player(s) cannot against each other
    :return int 3: player(s) do not exist
    """
    if r == 0: # First round
        if ex.binary_search_class(players[tk].get_players(),match.get_player_a()) is not None and ex.binary_search_class(players[tk].get_players(),match.get_player_b()) is not None:
            return 1  # Match valid
        else:
            return 3  # Player(s) don't exist
    else: # Check players have got through to the same round
        previous_winners = seasons[s].get_tournament(t).get_track(tk).get_round(r-1).get_winners()
        previous_winners.sort()
        player_a = ex.binary_search(previous_winners,match.get_player_a())
        player_b = ex.binary_search(previous_winners, match.get_player_b())
        if player_a is not None and player_b is not None:
            return 1  # Match valid
        else:
            return 2  # Players


def get_bonus_factor(track,difference):
    """
    Gets the bonus factor for the winner of a match
    :param Track track: the track
    :param int difference: the score difference in the match
    :return float factor: the bonus factor - 1 if not there
    """
    factor = 1
    for i in track.get_factors():
        if abs(int(difference)) == i.get_diff():
            factor = i.get_amount()
    return factor


def calculate_ranking_points_per_match(s_id,t_id,tk_id,r_id,match):
    """
    Calculates the ranking points per match
    Adds winner of the match to the round winner list
    Adds match to players in the match
    :param int s_id: season id
    :param int t_id: tournament id
    :param int tk_id: track id
    :param int r_id: round id
    :param Match match: the match
    :return: void
    """
    season = seasons[s_id]
    tournament = season.get_tournament(t_id)
    track = tournament.get_track(tk_id)
    round = track.get_round(r_id)
    current_pt = players[tk_id]

    # Find players
    p_1 = current_pt.get_player(ex.binary_search_class(current_pt.get_players(),match.get_player_a()))
    p_1.add_match(t_id,match)
    p_2 = current_pt.get_player(ex.binary_search_class(current_pt.get_players(),match.get_player_b()))
    p_2.add_match(t_id, match)
    # Score of players
    s_1 = match.get_a_score()
    s_2 = match.get_b_score()

    if s_1 > s_2:
        round.add_winner(match.get_player_a())
        factor = get_bonus_factor(track,s_1 - s_2)
        if len(track.get_rounds()) -1 == r_id:  # Final
            p_1.set_rank(p_1.get_rank(t_id) + (factor * season.get_ranking_point(r_id+1)), t_id)
        else: # Other round
            p_1.set_rank(p_1.get_rank(t_id) + (factor * season.get_ranking_point(r_id)), t_id)
        p_2.set_rank(p_2.get_rank(t_id) + season.get_ranking_point(r_id),t_id)  # Loser

    elif s_2 > s_1:
        round.add_winner(match.get_player_b())
        factor = factor = get_bonus_factor(track,s_2 - s_1)
        if len(track.get_rounds()) - 1 == r_id:  # Final
            p_2.set_rank(p_2.get_rank(t_id) + (factor * season.get_ranking_point(r_id+1)), t_id)
        else:  # Other round
            p_2.set_rank(p_2.get_rank(t_id) + (factor * season.get_ranking_point(r_id)), t_id)
        p_1.set_rank(p_1.get_rank(t_id) + season.get_ranking_point(r_id), t_id) # Loser


def encode_file(season,tournament,track,round):
    """
    Generates the file name for a match
    :param Season season: the season
    :param Tournament tournament: the tournament
    :param Track track: the track
    :param Round round: the round
    :return str filename: the filename of the match
    """
    return os.path.join(my_path, ".." + round_paths + "DADSA "+season.get_name()+" COURSEWORK B "+tournament.get_name()+" ROUND "+round.get_number()+" "+track.get_name()+".csv")


def read_matches_file(season,tournament,track,round,file):
    """
    Reads a whole round of matches
    :param Season season: the season
    :param Tournament tournament: the tournament
    :param Track track: the track
    :param Round round: the round
    :param str file: the file (normally from encode_file
    :return: void
    """
    s = ex.binary_search_class(seasons,season)
    t = ex.binary_search_class(seasons[s].get_tournaments(),tournament)
    tk = ex.binary_search_class(seasons[s].get_tournament(t).get_tracks(),track)
    max = seasons[s].get_tournament(t).get_track(tk).get_best_of()
    r = ex.binary_search_class(seasons[s].get_tournament(t).get_track(tk).get_rounds(),round)

    with open(file,'r') as csvFile:  # Open file
        reader = csv.DictReader(csvFile)
        line_num = 1  # Keep note of line number
        for row in reader:  # Loop on lines in file
            temp_match = Match(row["Player A"],int(row["Score Player A"]),row["Player B"],int(row["Score Player B"]))  # Create match
            if match_check_players(s,t,tk,r,temp_match) is 1:  # Players are allowed to play against each other
                temp_match = match_check(max, temp_match)  # Check match
                seasons[s].get_tournament(t).get_track(tk).get_round(r).add_match(temp_match)  # Add match to round
                calculate_ranking_points_per_match(s,t,tk,r,temp_match)  # Apply points
            else:
                print("One of the following players has not made it to this round: "+temp_match.get_player_a()+" "+temp_match.get_player_b())
                print("Line:"+str(line_num)+" in "+file)
            line_num += 1
    seasons[s].get_tournament(t).get_track(tk).get_round(r).set_status(2)  # Status set to complete
    if len(seasons[s].get_tournament(t).get_track(tk).get_rounds())-1 == r:
        # Last round in tournament
        set_ranking_points(s,t,tk)
        set_prize_money(s,t,tk)
        if len(seasons[s].get_tournaments()) - 1 == t:
            # Last round in last tournament
            print("Last round of last tournament")
        else:
            seasons[s].get_tournament(t+1).get_track(tk).get_round(0).set_status(1)
    else: # Set the current round to the next round
        seasons[s].get_tournament(t).get_track(tk).get_round(r+1).set_status(1)


def set_prize_money(s_id,t_id,tk_id):
    """
    To be called at the end of a tournament (track)
    Gives out prize money for the tournament to the players in the track
    :param int s_id: season id
    :param int t_id: tournament id
    :param int tk_id: track id
    :return: void
    """
    season = seasons[s_id]
    tournament = season.get_tournament(t_id)
    track = tournament.get_track(tk_id)
    while len(track.get_rounds())+1 > len(tournament.get_prize_money_all()):
        tournament.add_prize_money(0.0)  # Add 0.0 to the front of the list until the list is length of number of rounds
    tournament.sort_prize_money()

    r_id = 0  # Keep note of the current round index
    for r in track.get_rounds():  # Loop rounds
        previous_winners = track.get_round(r_id-1).get_winners()  # Hold previous winners
        for player in players[tk_id].get_players():  # Loop players
            # First round
            if ex.binary_search(r.get_winners(),player.get_name()) is None and r_id == 0:
                player.set_prize_money(tournament.get_prize_money(r_id), t_id)

            # Normal
            if ex.binary_search(r.get_winners(),player.get_name()) is None and ex.binary_search(previous_winners,player.get_name()) is not None:
                player.set_prize_money(tournament.get_prize_money(r_id),t_id)

            # Final - winner
            if ex.binary_search(r.get_winners(),player.get_name()) is not None and r_id == len(track.get_rounds())-1:
                player.set_prize_money(tournament.get_prize_money(len(tournament.get_prize_money_all())-1),t_id)
        r_id += 1


def set_ranking_points(s_id,t_id,tk_id):
    """
    To be called at the end of a tournament (track)
    Applies difficulty to the ranking points that players have (per tournament)
    :param int s_id: season id
    :param int t_id: tournament id
    :param int tk_id: track id
    :return: void
    """
    season = seasons[s_id]
    tournament = season.get_tournament(t_id)

    for player in players[tk_id].get_players():
        temp_rank = player.get_rank(t_id) * tournament.get_difficulty()
        player.set_rank(temp_rank,t_id)


def manual_input_match(season,tournament,track,round):
    """
    Method for manual input of a match
    :param Season season: the season
    :param Tournament tournament: the tournament
    :param Track track: the track
    :param Round round: the round
    :return: void
    """
    s = ex.binary_search_class(seasons, season)
    t = ex.binary_search_class(seasons[s].get_tournaments(), tournament)
    tk = ex.binary_search_class(seasons[s].get_tournament(t).get_tracks(), track)
    max = seasons[s].get_tournament(t).get_track(tk).get_best_of()
    r = ex.binary_search_class(seasons[s].get_tournament(t).get_track(tk).get_rounds(), round)

    print("PlayerA ScoreA PlayerB ScoreB")
    match_input = input("Enter the match: ")
    match_input = match_input.split(" ")  # Split the input into list that should be 4 length
    if len(match_input) == 4 and match_input[1].isdigit() and match_input[3].isdigit():
        p_a = match_input[0]
        a_s = int(match_input[1])
        p_b = match_input[2]
        b_s = int(match_input[3])
        temp_match = Match(p_a,a_s,p_b,b_s)
        if match_check_players(s, t, tk, r, temp_match) is 1:
            temp_match = match_check(max, temp_match)
            valid = True
            for m in seasons[s].get_tournament(t).get_track(tk).get_round(r).get_matches():
                if m.get_player_a() == temp_match.get_player_a() or m.get_player_a() == temp_match.get_player_b() or m.get_player_b() == temp_match.get_player_a() or m.get_player_b() == temp_match.get_player_b():
                    valid = False
            if valid is True:
                seasons[s].get_tournament(t).get_track(tk).get_round(r).add_match(temp_match)
                calculate_ranking_points_per_match(s, t, tk, r, temp_match)
                print("Match Successfully added")
            else:
                print("Players cannot play again in the same round")
        elif match_check_players(s, t, tk, r, temp_match) is 2:
            print("One of the following players has not made it to this round: "+temp_match.get_player_a()+" "+temp_match.get_player_b())
        elif match_check_players(s, t, tk, r, temp_match) is 3:
            print("At least one of the following players is not valid in this tournament "+temp_match.get_player_a()+" "+temp_match.get_player_b())
    else:
        print("Incorrect format")


def wins_with_score_tournament(t_id,difference,player):
    """
    Finds the number of wins that a player has with a certain score difference per tournament
    Winning 2:0 would be a score difference of 2
    :param int t_id: tournament id
    :param int difference: the score difference looking for
    :param Player player: the player in question
    :return int tally: the number of wins with the score difference
    """
    tally = 0
    player_name = player.get_name()
    for m in player.get_matches(t_id):
        if (m.get_player_a() == player_name and m.get_a_score() > m.get_b_score()) or (m.get_player_b() == player_name
                                                                                       and m.get_b_score() > m.get_a_score()):
            if abs(m.get_a_score() - m.get_b_score()) == difference:
                tally += 1
    return tally


def wins_with_score_season(season,difference,player):
    """
    Finds the number of wins that a player has with a certain score difference for the season
    Winning 2:0 would be a score difference of 2
    :param Season season: the season
    :param int difference: the score difference looking for
    :param Player player: the player in question
    :return int tally: the number of wins with the score difference
    """
    tally = 0  # Cheats by calling the tournament version of the method
    for t_id in range(0,len(season.get_tournaments())):
        tally += wins_with_score_tournament(t_id,difference,player)
    return tally


def percentage_wins_tournament(t_id,player):
    """
    The percentage of wins in a tournament for a player
    :param int t_id: tournament id
    :param Player player: the player in question
    :return float output: the percentage
    """
    played = 0
    wins = 0
    player_name = player.get_name()
    for m in player.get_matches(t_id):
        if m.get_player_a() == player_name:
            played += 1
            if m.get_a_score() > m.get_b_score():
                wins += 1
        elif m.get_player_b() == player_name:
            played += 1
            if m.get_b_score() > m.get_a_score():
                wins += 1
    output = 0.0
    if played != 0:
        output = round((wins / played) * 100, 2)
    return output


def percentage_wins_season(season,player):
    """
    The percentage of wins in a season for a player
    :param Season season: the season
    :param Player player: the player in question
    :return float output: the percentage of wins in the season
    """
    played = 0
    wins = 0
    player_name = player.get_name()
    for t_id in range(0,len(season.get_tournaments())):
        for m in player.get_matches(t_id):
            if m.get_player_a() == player_name:
                played += 1
                if m.get_a_score() > m.get_b_score():
                    wins += 1
            elif m.get_player_b() == player_name:
                played += 1
                if m.get_b_score() > m.get_a_score():
                    wins += 1
    output = 0.0
    if played != 0:
        output = round((wins / played) * 100, 2)
    return output


def player_with_most_wins(season,tk_id):
    """
    Finds the player with the most wins in a season per track
    :param Season season: the season
    :param int tk_id: track id
    :return List<str> players_most_wins: list of names of the player(s) with the highest number of wins
    """
    wins_per_player = []
    for p in players[tk_id].get_players():
        wins_per_player.append(0)

    # Loop matches
    for t in season.get_tournaments():
        for tk in t.get_tracks():
            for r in tk.get_rounds():
                for m in r.get_matches():
                    # Find id for players
                    p_a_id = ex.binary_search_class(players[tk_id].get_players(),m.get_player_a())
                    p_b_id = ex.binary_search_class(players[tk_id].get_players(), m.get_player_b())

                    # Find winner
                    if m.get_a_score() > m.get_b_score():
                        wins_per_player[p_a_id] = wins_per_player[p_a_id] + 1
                    else:
                        wins_per_player[p_b_id] = wins_per_player[p_b_id] + 1

    # Find the largest number of wins
    largest_value = wins_per_player[0]
    for p in wins_per_player:
        if largest_value < p:
            largest_value = p

    players_most_wins = []

    for i in range(0,len(wins_per_player)):
        if wins_per_player[i] == largest_value:
            players_most_wins.append(players[tk_id].get_player(i).get_name())

    return players_most_wins


def player_with_most_loses(season,tk_id):
    """
    Finds the player with the most loses in a season per track
    :param Season season: the season
    :param int tk_id: track id
    :return List<str> players_most_loses: list of names of the player(s) with the lowest number of wins
    """
    loses_per_player = []
    for p in players[tk_id].get_players():
        loses_per_player.append(0)

    # Loop matches
    for t in season.get_tournaments():
        for tk in t.get_tracks():
            for r in tk.get_rounds():
                for m in r.get_matches():
                    # Find id for players
                    p_a_id = ex.binary_search_class(players[tk_id].get_players(), m.get_player_a())
                    p_b_id = ex.binary_search_class(players[tk_id].get_players(), m.get_player_b())

                    # Find loser
                    if m.get_a_score() > m.get_b_score():
                        loses_per_player[p_b_id] = loses_per_player[p_b_id] + 1
                    else:
                        loses_per_player[p_a_id] = loses_per_player[p_a_id] + 1

    # Find the largest number of wins
    loses_count = loses_per_player[0]  # Unlikely the smallest value is larger than this number
    for p in loses_per_player:
        if loses_count < p:
            loses_count = p

    players_most_loses = []

    for i in range(0, len(loses_per_player)):
        if loses_per_player[i] == loses_count:
            players_most_loses.append(players[tk_id].get_player(i).get_name())

    return players_most_loses


def save():
    """
    Saves the programs status
    :return: void
    """
    pickle.dump(seasons, open("seasons_save.p", "wb"))
    pickle.dump(players, open("players_save.p", "wb"))

if start is True:

    quit_load = False
    if os.path.exists("seasons_save.p") is True:  # Check for previous save
        while quit_load == False:
            print("<>"*10)
            print("Do you want to load a previous save?")
            print("Last saved:"+time.strftime(" %H:%M:%S %d %B %Y",time.localtime(int(os.path.getmtime("seasons_save.p")))))
            print("1. YES")
            print("2. NO")
            user_load = input("> ")
            if user_load == "1":
                seasons = pickle.load(open("seasons_save.p", "rb"))
                players = pickle.load(open("players_save.p", "rb"))
                quit_load = True
            elif user_load == "2":
                read_settings()
                quit_load = True
    else:  # No save exists
        read_settings()
    options = ["SAVE & EXIT", "OUTPUT INFO ABOUT TENNIS", "VIEW CURRENT DATA", "CONTINUE"]
    # Actual user input related
    quit = False
    while quit is not True:
        print("████████████")
        print("<--| MAIN MENU |-->")
        print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        print("Options:")
        i = 0
        while i < len(options):
            print(str(i) + ".", options[i])
            i += 1


        user = input("Enter command: ")
        if user == "quit" or user == "q" or user == "0":
            quit = True
            print("SAVING")
            save()
            print("EXITING")
        elif user == "1":  # output info
            print("\n----INFORMATION----")
            for i in seasons:
                print(str(i))
        elif user == "2":
            data_quit = False
            while data_quit is not True:
                print("\n-----CURRENT DATA-----")
                options_data = ["Main Menu", "View ranking", "View prize money", "Number of wins for a player with a particular score",
                                "Percentage wins for a player", "Player with most wins", "Player with most loses"]
                i = 0
                while i < len(options_data):
                    print(str(i) + ".", options_data[i])
                    i += 1
                user_data = input("Enter command: ")
                if user_data == "0":
                    data_quit = True
                elif user_data == "1":
                    print("\nRanking:")
                    for pt in players:
                        print(pt.get_name() + " ("+pt.get_type()+")")
                        temp = []
                        for player in pt.get_players():
                            temp.append(player)
                        temp.sort(key=lambda obj: obj.get_total_ranking(), reverse=True)
                        num = 1
                        for t in temp:
                            print("%02d"%(num)+". "+t.get_name() + " | " + str(t.get_total_ranking()))
                            num += 1
                elif user_data == "2":
                    print("\nPrize Money:")
                    for pt in players:
                        print(pt.get_name() + " (" + pt.get_type() + ")")
                        temp = []
                        for player in pt.get_players():
                            temp.append(player)
                        temp.sort(key=lambda obj: obj.get_total_prize_money(), reverse=True)
                        num = 1
                        for t in temp:
                            print("%02d"%(num)+". "+t.get_name() + " | $" + "{:,}".format(t.get_total_prize_money()))
                            num += 1
                elif user_data == "3":
                    print("\nNumber of wins per player with a particular score:")
                    tk_count = 1
                    for t in players:
                        print(str(tk_count) + ".", t.get_name())
                        tk_count += 1
                    user_tk = input("Enter number for track: ")
                    if user_tk.isdigit() and int(user_tk)-1 < len(players) and int(user_tk) != 0:
                        user_tk = int(user_tk)-1
                        for player in players[user_tk].get_players():
                            print(player.get_name())
                        user_player = input("Please enter a player's name from the list above: ")
                        search_player = ex.binary_search_class(players[user_tk].get_players(),user_player)
                        if search_player is not None: # Player exists
                            print("0. Season")
                            t_count = 1
                            for t in seasons[0].get_tournaments():
                                print(str(t_count) + ".", t.get_name())
                                t_count += 1
                            user_tourn = input("Enter number for tournament: ")
                            if user_tourn == "0":
                                # selected season
                                print("Example of points difference: 2:0 -> difference = 2")
                                print("Example of points difference: 2:1 -> difference = 1")
                                user_score = input("Please enter a score difference: ")
                                if user_score.isdigit() and int(user_score) > 0:
                                    print("The number of wins where "+players[user_tk].get_player(search_player).get_name() +" has scored with a points difference of "+user_score +" in season "+seasons[0].get_name()+" is " +str(wins_with_score_season(seasons[0],int(user_score),players[user_tk].get_player(search_player))))
                            elif user_tourn.isdigit() and int(user_tourn)-1 < len(seasons[0].get_tournaments()):
                                # selected a tournament
                                user_tourn = int(user_tourn)-1
                                print("Example of points difference: 2:0 -> difference = 2")
                                print("Example of points difference: 2:1 -> difference = 1")
                                user_score = input("Please enter a score difference: ")
                                if user_score.isdigit() and int(user_score) > 0 and int(user_score) <= int(seasons[0].get_tournament(user_tourn).get_track(user_tk).get_best_of()):
                                    print("The number of wins where "+players[user_tk].get_player(search_player).get_name() +" has scored with a points difference of "+ user_score +" is " + str(wins_with_score_season(seasons[0],int(user_score),players[user_tk].get_player(search_player))))
                                else:
                                    print("Invalid score")
                        else:
                            print("Player is not valid")
                elif user_data == "4":
                    print("Percentage wins for a player:")
                    tk_count = 1
                    for t in players:
                        print(str(tk_count) + ".", t.get_name())
                        tk_count += 1
                    user_tk = input("Enter number for track: ")
                    if user_tk.isdigit() and int(user_tk)-1 < len(players) and int(user_tk) != 0:
                        user_tk = int(user_tk)-1
                        for player in players[user_tk].get_players():
                            print(player.get_name())
                        user_player = input("Please enter a player's name from the list above: ")
                        search_player = ex.binary_search_class(players[user_tk].get_players(), user_player)
                        if search_player is not None:  # Player exists
                            t_count = 1
                            print("0. Season")
                            for t in seasons[0].get_tournaments():
                                print(str(t_count) + ".", t.get_name())
                                t_count += 1
                            user_tourn = input("Enter number for tournament: ")
                            if user_tourn == "0":
                                # selected season
                                print("The percentage wins for " + players[user_tk].get_player(search_player).get_name() + " in " + seasons[0].get_name() + " is " + str(percentage_wins_season(seasons[0],players[user_tk].get_player(search_player))) + "%")
                            elif user_tourn.isdigit() and int(user_tourn)-1 < len(seasons[0].get_tournaments()):
                                # selected a tournament
                                user_tourn = int(user_tourn)-1
                                print("The percentage wins for "+players[user_tk].get_player(search_player).get_name()+" in "+seasons[0].get_tournament(user_tourn).get_name()+" is "+str(percentage_wins_tournament(user_tourn,players[user_tk].get_player(search_player)))+"%")

                elif user_data == "5":
                    print("Player with most wins")
                    tk_count = 1
                    for t in players:
                        print(str(tk_count) + ".", t.get_name())
                        tk_count += 1
                    user_tk = input("Enter number for track: ")
                    #pr = cProfile.Profile()
                    #pr.enable()
                    if user_tk.isdigit() and int(user_tk)-1 < len(players) and int(user_tk) != 0:
                        print("The player(s) with the most wins in the season")
                        for i in player_with_most_wins(seasons[0],int(user_tk)-1):
                            print("- "+i)
                    #pr.disable()
                    #pr.print_stats()
                elif user_data == "6":
                    print("Player with most loses")
                    tk_count = 1
                    for t in players:
                        print(str(tk_count) + ".", t.get_name())
                        tk_count += 1
                    user_tk = input("Enter number for track: ")
                    if user_tk.isdigit() and int(user_tk)-1 < len(players) and int(user_tk) != 0:
                        print("The player(s) with the most loses in the season")
                        for i in player_with_most_loses(seasons[0], int(user_tk)-1):
                            print("-" + i)

        elif user == "3":
            con = False
            while con is not True:
                print("\n--CONTINUING--")
                t_count = 1
                print("0. MAIN MENU")
                for t in seasons[0].get_tournaments():
                    print(str(t_count) + ".", t.get_name())
                    t_count += 1

                user_tourn = input("Enter number for tournament: ")
                tk_count = 1
                if user_tourn == "0":
                    con = True # Quit
                elif user_tourn.isdigit() and int(user_tourn)-1 < len(seasons[0].get_tournaments()):
                    user_tourn = int(user_tourn)-1
                    print("Selected: "+seasons[0].get_tournament(user_tourn).get_name())
                    print("Available tracks:")
                    for t in seasons[0].get_tournament(user_tourn).get_tracks():
                        print(str(tk_count) + ".", t.get_name())
                        tk_count += 1
                    user_tk = input("Enter number for track: ")
                    if user_tk.isdigit() and int(user_tk)-1 < len(
                            seasons[0].get_tournament(user_tourn).get_tracks())and int(user_tk) != 0:
                        user_tk = int(user_tk)-1
                        quit_rounds = False
                        while quit_rounds is not True:
                            round_index = 0
                            current_round = 0
                            set = 0
                            for r in seasons[0].get_tournament(user_tourn).get_track(user_tk).get_rounds():
                                if r.get_status() == 1:
                                    current_round = round_index
                                    set = 1
                                round_index += 1
                            if set != 0:
                                print("\nCurrent round is Round "+seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).get_name())
                                print("Options are:")
                                print("0. Select tournament (back)")
                                print("1. Read from file")
                                print("2. Manual input")

                                user_round_option = input("> ")
                                if user_round_option == "0":
                                    quit_rounds = True
                                elif user_round_option == "1":
                                    # read round from file
                                    read_matches_file(seasons[0].get_name(),seasons[0].get_tournament(user_tourn).get_name(),seasons[0].get_tournament(user_tourn).get_track(user_tk).get_name(),seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).get_name(),
                                                      encode_file(seasons[0], seasons[0].get_tournament(user_tourn),
                                                                  seasons[0].get_tournament(user_tourn).get_track(user_tk),
                                                                  seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round)))
                                elif user_round_option == "2":
                                    # Manual input for insane people
                                    user_input = True
                                    while user_input is True:
                                        if len(seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).get_matches()) == \
                                                seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).get_max_matches():
                                            user_input = False
                                            seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).set_status(2)
                                            if len(seasons[0].get_tournament(user_tourn).get_track(user_tk).get_rounds()) - 1 == current_round:
                                                # Last round in tournament
                                                set_ranking_points(0, user_tourn, user_tk)
                                                set_prize_money(0, user_tourn, user_tk)
                                                if len(seasons[0].get_tournaments()) - 1 == user_tourn:
                                                    # Last round in last tournament
                                                    print("Last round of last tournament")
                                                else:
                                                    seasons[0].get_tournament(user_tourn + 1).get_track(user_tk).get_round(0).set_status(1)

                                            else:  # Set the current round to the next round
                                                seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round + 1).set_status(
                                                    1)
                                            set = 1

                                        else:
                                            if current_round == 0:
                                                available_players = []
                                                for p in players[user_tk].get_players():
                                                    available_players.append(p.get_name())
                                            else:
                                                available_players = sorted(seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round-1).get_winners())
                                            for m in seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).get_matches():
                                                available_players.remove(m.get_player_a())
                                                available_players.remove(m.get_player_b())
                                            print("\nPlayers that can play in this round:")
                                            print(available_players)
                                            manual_input_match(seasons[0].get_name(),seasons[0].get_tournament(user_tourn).get_name(),seasons[0].get_tournament(user_tourn)
                                                               .get_track(user_tk).get_name(),seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round)
                                                               .get_name())


                                if seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).get_status() != 1:
                                    print("Players through to the next round:")
                                    for p in seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(current_round).get_winners():
                                        print(p)
                            else:
                                quit_rounds = True
                                completed = False
                                for i in seasons[0].get_tournament(user_tourn).get_track(user_tk).get_round(round_index-1).get_winners():
                                    print("The winner of "+seasons[0].get_tournament(user_tourn).get_name()+" was "+i+" ("+seasons[0].get_tournament(user_tourn).get_track(user_tk).get_name()+")")
                                    completed = True
                                    print("Ranking for this tournament:")
                                    print("Player | points | prize money")
                                    temp = []
                                    for p in players[user_tk].get_players():
                                        temp.append(p)
                                    temp.sort(key=lambda obj: obj.get_rank(user_tourn), reverse=True)
                                    rank = 1
                                    for t in temp:
                                        print("%02d"%(rank)+". "+t.get_name() + " | "+str(t.get_rank(user_tourn))+" | $"+"{:,}".format(t.get_prize_money(user_tourn)))
                                        rank += 1
                                    print("<><>End of tournament<><>")

                                if completed is False:
                                    print("Please complete previous tournaments first")


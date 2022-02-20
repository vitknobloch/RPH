# This script creates two (identical) players, 
# lets them play for some number of iterations and 
# then displays their scores. 
#
# For running this script, you need to put the 'game.py'
# as well as your 'player.py' to the python path, e.g. 
# to the the working directory. 
#
# A very simple testing script, feel free to modify it
# according to your needs
#
# example code for students of B4B33RPH course
# Author: Tomas Svoboda, and the RPH team

from game import Game 

# assuming your player is in player.py as required
# https://cw.fel.cvut.cz/wiki/courses/b4b33rph/cviceni/veznovo_dilema/specifikace
import player
import player_louny
import player_dummyCOOP
import player_dummyDEFECT
from copy import copy


def run_game(number_of_iterations, playerA, playerB, payoff_matrix):

    # create the game instance
    my_game = Game(playerA, playerB, payoff_matrix, number_of_iterations, True)
    # run game
    my_game.run()

    # get scores 
    scores = my_game.get_players_payoffs()

    # display scores
    print('', playerA.name, 'got:',scores[0], '\n', playerB.name, 'got:', scores[1], '\n----------------')

    return scores

if __name__ == '__main__':
    # define the payoff matrix; see game.py for detailed explanation of this matrix
    coop = 4
    defect = 2
    win = 6
    lose = 1

    payoff_matrix = ( ((coop,coop),(lose,win)) , ((win,lose),(defect,defect)) )

    # define the number of iterations
    number_of_iterations = 20


    players = [
        player, 
        player_louny, 
        player_dummyCOOP, 
        player_dummyDEFECT
        ]

    players_names = [
        "Vita",
        "Louny",
        "Coop",
        "Defect"
    ]

    players_points = []
    for p in players: 
        players_points.append(0)

    for i in range(len(players)):
        for j in range(i, len(players)):
            p1 = players[i].MyPlayer(payoff_matrix, number_of_iterations)
            p2 = players[j].MyPlayer(payoff_matrix, number_of_iterations)
            p1.name = players_names[i]
            p2.name = players_names[j]
            points = run_game(number_of_iterations, p1, p2, payoff_matrix)
            players_points[i] += points[0]
            players_points[j] += points[1]

    print(players_points)



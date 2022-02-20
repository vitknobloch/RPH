import random_player
from game_board import GameBoard
import time
import player_final as player
import random

HOW_MANY_ITERATIONS = 10000


class HeadlessReversiCreator(object):
    '''
    Creator of the Reversi game without the GUI.
    '''

    def __init__(self, player1, player1_color, player2, player2_color, board_size=8):
        '''
        :param player1: Instance of first player
        :param player1_color: color of player1
        :param player2: Instance of second player
        :param player1_color: color of player2
        :param boardSize: Board will have size [boardSize x boardSize]
        '''
        self.board = GameBoard(board_size, player1_color, player2_color)
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.current_player_color = player1_color
        self.player1_color = player1_color
        self.player2_color = player2_color

    def play_game(self):
        '''
        This function contains game loop that plays the game.
        '''
        # TODO: Time limit for move
        correct_finish = True
        while self.board.can_play(self.current_player_color):
            startTime = time.time()
            move = self.current_player.move(self.board.get_board_copy())
            endTime = time.time()
            moveTime = (endTime - startTime) * 1000
            if move is None:
                print('Player %d reurns None istead of a valid move. Move takes %.3f ms.' % (
                    self.current_player_color, moveTime))
                correct_finish = False
                break

            move = (int(move[0]), int(move[1]))
            if self.board.is_correct_move(move, self.current_player_color):
                self.board.play_move(move, self.current_player_color)

            else:
                print('Player %d made the wrong move [%d,%d]' % (
                    self.current_player_color, move[0], move[1]))
                correct_finish = False
                break
            self.change_player()
            if not self.board.can_play(self.current_player_color):
                self.change_player()

          #  self.board.print_board()
        if correct_finish:
            return self.printFinalScore()
        else:
            if self.current_player_color == self.player1_color:
                print('Winner is player %d.' % (self.player2_color))
            else:
                print('Winner is player %d.' % (self.player1_color))

    def change_player(self):
        '''
        Change the current_player
        '''
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.current_player_color = self.player2_color
        else:
            self.current_player = self.player1
            self.current_player_color = self.player1_color

    def printFinalScore(self):
        p1Stones = 0
        p2Stones = 0
        for x in range(self.board.board_size):
            for y in range(self.board.board_size):
                if self.board.board[x][y] == 0:
                    p1Stones += 1
                if self.board.board[x][y] == 1:
                    p2Stones += 1

        if p1Stones > p2Stones:
            return 1
        elif p2Stones > p1Stones:
            return 2
        elif p2Stones == p1Stones:
            return 0


if __name__ == "__main__":
    p1_color = 0
    p2_color = 1

    p1 = random_player.MyPlayer(p1_color, p2_color)
    results = {0: 0, 1: 0, 2: 0}
    for i in range(HOW_MANY_ITERATIONS):
        start = time.time()
        p2 = player.MyPlayer(p2_color, p1_color)
        game = HeadlessReversiCreator(p1, p1_color, p2, p2_color, 8)
        results[game.play_game()] += 1
        if i % 10 == 0:
            print(f'{str(i).zfill(4)} - {int((time.time()-start)*1000)}ms')

    print(
        f'Draws: {results[0]}; random wins: {results[1]}; player wins: {results[2]}')

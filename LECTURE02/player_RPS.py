import random

OPPOSITE_MOVES = dict(R='P', P='S', S='R')
POSSIBLE_MOVES = tuple(OPPOSITE_MOVES.keys())

class BasePlayer:
    def __init__(self):
        self.opp_moves = []
        self.my_moves = []

    def play(self):
        my_move = self.find_move()
        self.my_moves.append(my_move)
        return my_move

    def find_move(self):
        raise NotImplementedError

    def record_opp_move(self, opp_move):
        self.opp_moves.append(opp_move)

    def __str__(self):
        return self.__class__.__name__


class RandomPlayer(BasePlayer):
    def find_move(self):
        return random.choice(POSSIBLE_MOVES)


class SmartPlayer(BasePlayer):
    def find_move(self):
        if len(self.opp_moves) > 0:
            return random.choice(map(OPPOSITE_MOVES.get, self.opp_moves))
        else:
            return random.choice(POSSIBLE_MOVES)


if __name__ == "__main__":
    p = RandomPlayer()
    for i in range(10):
        print(p.play())
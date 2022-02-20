import random

class MyPlayer:
    """Player plays around corners and changes strategy when needed"""
    def __init__(self, my_color, opp_color):
        self.name = "louckada"
        self.my_color = my_color
        self.opp_color = opp_color
        self.turn_num = 0
        
    def move (self, board):
        """checks all spaces for viable moves, chooses best one"""
        values_of_moves = []
        possible_moves = []
        non_danger_moves = []

        for row in range(0, len(board)):
            for col in range(0, len(board)):
                if (self.validate_move(row, col, board, values_of_moves)):
                    possible_moves.append((row, col))

        print(possible_moves)
        print(values_of_moves)

        self.turn_num += 1
        self.avoid_giving_corner(possible_moves, values_of_moves)

        for i in range (len(values_of_moves)):
            if (values_of_moves[i] != 0):
                non_danger_moves.append(possible_moves[i])

        corner_move = self.corner_possible(possible_moves)
        max_move = self.find_max_value(values_of_moves)

        print(possible_moves)
        print(values_of_moves)

        if (corner_move != False):
            return corner_move
        elif (self.turn_num > 10):
            return possible_moves[max_move]
        else:
            if(non_danger_moves == []):
                return random.choice(possible_moves)
            return random.choice(non_danger_moves)


    def validate_move(self, row, col, board, values_of_moves):
        """checks if a move is valid"""
        if (board[row][col] == -1):
            if (self.find_move(row, col, board, values_of_moves)):
                return True
        else:
            return False
                    

    def find_move(self, row, col, board, values_of_moves):
        """finds all possible moves"""
        value_of_move = 0
        for ri in range(row-1, row+2):
            for ci in range(col-1, col+2):
                if (self.goes_beyond_borders(ri, ci, board)): continue

                if (board[ri][ci] == self.opp_color):
                    diff_r =  ri - row
                    diff_c =  ci - col
                    temp_diff_r = 0
                    temp_diff_c = 0
                    temp_value = 0  #value_of_move shows how many stones will be captured

                    while (board[ri + temp_diff_r][ci + temp_diff_c] == self.opp_color):
                        #tries to find all stones of opponents color in a row
                        temp_diff_c += diff_c
                        temp_diff_r += diff_r
                        temp_value += 1

                        if (self.goes_beyond_borders(ri + temp_diff_r, ci + temp_diff_c, board)): break
                        
                        if(board[ri + temp_diff_r][ci + temp_diff_c] == self.my_color):
                            #adding the move to a list of all moves
                            value_of_move += temp_value
                            
        if (value_of_move == 0):
            return False
        else: 
            values_of_moves.append(value_of_move)
            return True

    def find_max_value(self, values):
        """finds max value in a list of values"""
        n = 0
        max_num = 0 
        for num in range(0, len(values)):
            if(values[num] > max_num):
                n = num
                max_num = values[num]
        return n

    def corner_possible(self, moves):
        """checks if any corner-capture is possible"""
        for i in range (0, len(moves)):
            if (moves[i] == (0, 0)):
                return moves[i]

            if (moves[i] == (len(moves), 0)):
                return moves[i]

            if (moves[i] == (0, len(moves))):
                return moves[i]

            if (moves[i] == (len(moves), len(moves))):
                return moves[i]
        return False

    def avoid_giving_corner(self, moves, values):
        dangerous_moves = [(0,1), (1,1), (1,0), (6,0), (6,1), (7,1), (0,6), (1,6), (1,7), (6,6), (6,7), (7,6)]
        for i in range(len(moves)):
            for j in dangerous_moves:
                if (moves[i] == j):
                    values[i] = 0

    def detect_dangerous_move(self, move):
        dangerous_moves = [(0,1), (1,1), (1,0), (6,0), (6,1), (7,1), (0,6), (1,6), (1,7), (6,6), (6,7), (7,6)]
        for i in dangerous_moves:
            if (i == move):
                return True
        return False

    def goes_beyond_borders(self, row, column, board):
        """Checks if we reach beyond borders of matrix"""
        if (row < 0 or column < 0): return True
        if (row >= len(board) or column >= len(board)): return True
        else: return False
    

if __name__ == "__main__":
    board =[[-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1,  1, -1, -1],
            [-1, -1,  0,  0,  0,  0,  0, -1],
            [-1, -1,  0,  1,  1, -1,  1, -1],
            [-1,  0, -1,  0,  0, -1, -1, -1],
            [-1, -1, -1,  0, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1]]
    p1 = MyPlayer(1, 0)
    fin_move = p1.move(board)
    print (fin_move)



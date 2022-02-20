import copy
import random

#evaluate_move() constants
CORNER_VALUE = 100
POSSIBLE_MOVE_VALUE = 4
BOARD_VALUE = 0.33
#evaluate_board() constants
EDGE_MULTIPLYER = 3
CORNER_MULTIPLYER = 3

class MyPlayer:
    '''Evaluate each possible move and choose the best one'''
 
    def __init__(self, my_color, opponent_color):
        '''
        Params:
        my_color: color of this players stones (0 or 1)
        opponent_color: color of opponents stones (0 or 1)
        '''
        self.name = 'knoblvit'
        self.my_color = my_color
        self.op_color = opponent_color
 
  
    def move(self, board):
        '''Return players next move position'''
        #initialize new instance of Board class
        b = Board(board)
 
        #get list of all possible moves
        pm = b.find_possible_moves(self.my_color)
 
        if len(pm) == 0:
            return None
        elif len(pm) == 1:
            return pm[0]
         
        #evaluate all the possible moves
        moves_eval = []
        for m in pm:
            move_value = b.evaluate_move(m, self.my_color)
 
            #subtract eval of opponents best move next round
            bm = Board(copy.deepcopy(board), b.corners, b.corners_adjescent, b.free_count)
            bm.flip_all(m, self.my_color)
            opm = bm.find_possible_moves(self.op_color)
            if len(opm) == 0:
                moves_eval.append(move_value)
                continue
 
            op_moves_eval = []
            for om in opm:
                op_moves_eval.append(bm.evaluate_move(om, self.op_color))
 
            move_value -= self.pick_best_move(opm, op_moves_eval)[1]
 
            moves_eval.append(move_value)
         
        return self.pick_best_move(pm, moves_eval)[0]        
 
 
    def pick_best_move(self, possible_moves, moves_eval):
        '''Picks the best move from possible moves'''
        #pick the best one (with highest evaluation value)
        best_move_index = 0
        best_move = []
        for i in range(len(moves_eval)):
            if moves_eval[i] > moves_eval[best_move_index]:
                best_move_index = i
                best_move = [possible_moves[i]]
            elif moves_eval[i] == moves_eval[best_move_index]:
                best_move.append(possible_moves[i])
 
        #return random move from the ones with highest evaluation
        return random.choice(best_move), moves_eval[best_move_index]
 
 
 
class Board:
    '''
    This class takes care of all the computing connected with board evaluation
    '''
 
    def __init__(self, board, corners = None, corners_adjescent = None, \
        free_count = None):
        '''
        Params:
        board: the board values list
        corners: (optional) list of corners of the board
        corners_adjescent: (optional) list of positions next to the corners
        '''
        self.board = board
        self.board_size = len(board)
        self.corners = self.get_corners() if corners == None else corners           
        self.corners_adjescent = self.get_corners_adjescent() \
            if corners_adjescent == None else corners_adjescent
        self.free_count = self.get_free_tiles_count() if free_count == None \
            else free_count
                 
 
    def evaluate_move(self, move, color):
        '''
        Evaluates the move and return an integer based on the moves quality
        '''
        move_value = 0
         
        #if move is corner (+100)
        if move in self.corners:
            move_value += CORNER_VALUE
 
        #if move is next to free corner (-100)
        for ca in self.corners_adjescent:
            if move in ca and move != ca[0]:
                if self.board[ca[0][0]][ca[0][1]] == -1:
                    move_value -= CORNER_VALUE
 
        #find count of possible moves of player and opponent after the move
        b = Board(copy.deepcopy(self.board), self.corners, \
            self.corners_adjescent, self.free_count)
        b.flip_all(move, color)
 
        pm_color = b.find_possible_moves(color)
        pm_opponent = b.find_possible_moves(1-color)
        #add my move options and subtract opponents
        move_value += POSSIBLE_MOVE_VALUE * (len(pm_color) - len(pm_opponent))
 
        if b.free_count > 0:
            #board evaluation becomes more important towards the end of the game
            board_val_importance = (b.board_size**2 / b.free_count**2)
 
            #add multiplyed board value to the move_value
            board_val = b.evaluate_board(color) * board_val_importance * BOARD_VALUE
            move_value += round(board_val)
 
        return move_value
 
 
    def evaluate_board(self, color):
        '''
        Evaluate the current board state
        Params:
        color: Color of the player for who the board should be evaluated
        '''
        board_val = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                #For every tile on the board
 
                if self.board[x][y] == -1:
                    continue
                 
                tile_val = 1
 
                #if the tile is edge tile
                if x == 0 or y == 0 or \
                    x == self.board_size -1 or y == self.board_size -1:
 
                    tile_val *= EDGE_MULTIPLYER
                #if the tile is corner tile
                if (x, y) in self.corners:
                    tile_val *= CORNER_MULTIPLYER
 
                #add or subtract based on whether the stone is my or opponents
                if self.board[x][y] == color:
                    board_val += tile_val
                elif self.board[x][y] == (1-color):
                    board_val -= tile_val
 
        return board_val
 
 
    def get_corners(self):
        '''Return list of corners of this board'''
        return [(0,0), (0, self.board_size-1), (self.board_size-1, 0), \
            (self.board_size-1, self.board_size-1)]
 
 
    def get_corners_adjescent(self):
        '''Return list of corners with tiles adjescent to them of this board'''
        corners_adjescent = [] #2D array
        for c in self.corners:
            ca = [c] #add the corner to the first place
            for i in range(-1, 2):
                for j in range(-1, 2):
                    #don't add the corner again
                    if i != 0 or j != 0:
                        x = c[0] + i
                        y = c[1] + j
                        #add the tile if it's not out of the board
                        if (x >= 0 and x < self.board_size and \
                            y >= 0 and y < self.board_size):
 
                            ca.append((x, y))
            #add the list for this corner to the 2D list
            corners_adjescent.append(ca)
         
        return corners_adjescent
 
 
    def get_free_tiles_count(self):
        '''Returns the number of free tiles on the board'''
        counter = 0
        for r in self.board:
            for t in r:
                if t == -1:
                    counter += 1
 
        return counter
 
    def get_score(self):
        '''Returns tuple (number of stones '0', number of stones '1')'''
        score0 = 0
        score1 = 1
 
        for r in self.board:
            for t in r:
                if t == 0:
                    score0 += 1
                elif t == 1:
                    score1 += 1
 
        return (score0, score1)
     
 
    def find_possible_moves(self, color):
        '''
        Iterate through the board and find all moves possible
        Params:
        color: color of the player whose moves should be found
        '''
        possible_moves = []
 
        for x in range(self.board_size):
            for y in range(self.board_size):
                #skip tile if it's not empty
                if self.board[x][y] != -1:
                    continue               
                #test the tile
                if self.all_possible_flips((x, y), color) > 0:
                    possible_moves.append((x, y))
         
        return possible_moves
 
    def flip_all(self, position, color):
        '''
        Change the board according to the moves target position
        Params:
        position: tuple (row, column) with the coordinates of the move
        color: color of the player who played the move
        '''
        self.board[position[0]][position[1]] = color
        for i in range(-1, 2):
            for j in range(-1, 2):
                #get number of stones to be flipped in given direction
                count = self.possible_flips_directional(position, (i, j), color)
                #if there are stones to be flipped
                if count > 0:
                    self.flip_directional(position, (i, j), color, count)
         
        self.free_count = self.get_free_tiles_count()
     
    def flip_directional(self, position, direction, color, count):
        '''
        Flip the given number stones from the given position in the given direction
        Params:
        position: tuple (row, column) with the coordinates of the move
        direction: tuple (row, column) vector in the desired direction
        color: color to flip the stones to
        count: how many stones should be flipped (positon stone excluded)
        '''
        x = position[0] + direction[0]
        y = position[1] + direction[1]
 
        for i in range(count):
            self.board[x][y] = color
            x += direction[0]
            y += direction[1]
             
 
    def all_possible_flips(self, position, color):
        '''
        Get the number flip possible in all directions
        Params:
        positon: tuple (row, column) with the coordinates of the move
        color: color of player whose possible flips should be counted
        '''
        counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                counter += self.possible_flips_directional(position, (i, j), color)
         
        return counter
 
    def possible_flips_directional(self, position, direction, color):
        '''
        Get the number of flips possible in the given direction
        Params:
        position: tuple (row, column) with the coordinates of the move
        direction: tuple (row, column) vector in the desired direction
        color: color to flip the stones to
        '''
        x = position[0] + direction[0]
        y = position[1] + direction[1]
 
        counter = 0
        #while the position is on the board
        while x >= 0 and y >= 0 and x < self.board_size and y < self.board_size:
 
            #return the counter when found same-coloured stone
            if self.board[x][y] == color:
                return counter
 
            #return 0 if there is an empty square on the other side of the sequence
            elif self.board[x][y] == -1:
                return 0
 
            #move to next tile in the direction if there is opponets stone
            elif self.board[x][y] == (1-color): # (1-color)--> opponent color
                x += direction[0]
                y += direction[1]
                counter += 1
         
        #if there wasn't same colored stone until the edge of board
        return 0
     
    def print_board(self):
        '''
        Debug and output method to print the board and score
        '''
        #count the score
        count0 = 0
        count1 = 0
        #print the board
        for i in range(self.board_size + 1):
            print('* ', end="")
        print('*')
        for r in self.board:
            print('*', end="")
            for p in r:
                if p == -1:
                    print('░░', end="")
                elif p == 0:
                    count0 += 1
                    print(' X', end="")
                elif p == 1:
                    count1 += 1
                    print(' O', end="")
            print(' *')
        for i in range(self.board_size + 1):
            print('* ', end="")
        print('*')
 
        #print the score
        print("Score of player0:", count0)
        print("Score of player1:", count1)
 
 
if __name__ == '__main__':
    #init test board and players
    board = [
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1,  1,  0, -1, -1, -1],
        [-1, -1, -1,  0,  1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1]]
 
    b = Board(board)    
    p0 = MyPlayer(0, 1)
    p1 = MyPlayer(1, 0)
 
    for r in board: print(r)
    print('------------')
    p0.move(board)
    for r in board: print(r)
    print('------------')
 
    #play 30 rounds
    for i in range(35):
        if len(b.find_possible_moves(p0.my_color)) > 0 :
            m0 = p0.move(b.board)
            b.flip_all(m0, p0.my_color)
            #print("0:", m0)
            #b.print_board()
         
        if len(b.find_possible_moves(p1.my_color)) > 0 :
            m1 = p1.move(b.board)
            b.flip_all(m1, p1.my_color)
            #print("1:", m1)
            #b.print_board()
     
    b.print_board()
 
    board = [
    [-1,1,  1,  1,  1,  1,  0,  0],
    [0, 1,  0,  0,  0,  0,  0,  0],
    [1, 1,  1,  1,  1,  1,  0,  0],
    [1, 1,  0,  1,  0,  1,  0,  0],
    [1, 1,  0,  0,  1,  0,  0,  0],
    [0, 0,  0,  1,  1,  1,  0,  0],
    [0, 0,  1,  1,  1,  0,  1,  0],
    [0, 1,  1,  1,  1,  1,  1,  1]]
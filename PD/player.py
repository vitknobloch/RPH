#CONSTANTS for readability
COOPERATE = False
DEFECT = True

STRAT_COOP = 1
STRAT_DEFECT = 2
STRAT_ALTERNATE = 3
STRAT_ALWAYS_COOP = 4


class MyPlayer:
    '''Player chooses strategy based on matrix, mostly repeat opponents'''

    def __init__(self, payoff_matrix, number_of_iterations = 0):
        '''
        Initialize important properties, set strategy based on matrix

        Arguments: \n
        payoff_matrix -- Payoff_matrix for this game of PD \n
        number_of_iterations -- the number of rounds in this game of PD (0 means undefined) (default 0)
        '''
        self.payoff_matrix = payoff_matrix
        self.strategy = self.analyze_matrix(payoff_matrix)
        #strategy value (COOP = 1, DEFECT = 2, ALTERNATE = 3, ALWAYS_COOP = 4)      

        self.number_of_iterations = number_of_iterations
        self.round_counter = 0

        self.my_last_move = None
        self.signal_noise = 0
        self.my_moves = []
        self.opponent_moves = []

    def move(self):
        '''
        Decide a move. return True for DEFECT and False for COOPERATE
        '''
        self.round_counter += 1
        my_move = COOPERATE

        if(self.strategy == STRAT_COOP):
            my_move = self.move_coop()

        elif(self.strategy == STRAT_DEFECT):
            my_move = self.move_defect()

        elif(self.strategy == STRAT_ALTERNATE):
            my_move = self.move_alternate()

        elif(self.strategy == STRAT_ALWAYS_COOP):
            my_move = self.move_always_coop()

        self.my_last_move = my_move
        return my_move

    def record_last_moves(self, my_last_move, opponent_last_move):
        '''
        Recieve last moves of myself and the opponent and store them for strategical decisions.

        Arguments:\n
        my_last_move -- True for DEFECT, False for COOPERATE \n
        opponent_last_move -- True for DEFECT, False for COOPERATE
        '''
        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)

        if len(self.my_moves) > 5:
            self.my_moves.pop(0)
            self.opponent_moves.pop(0)

        #if my last answer was flipped, set round counter to forgiveness to 2 rounds
        if my_last_move != self.my_last_move:
            self.signal_noise = 2


    #COOP until opponent cooperates
    def move_coop(self):
        '''Decide a move if the strategy is COOP, return bool'''
        #Always defect on last 2 turns if WIN is better than COOP
        if (self.number_of_iterations != 0) and (self.round_counter > self.number_of_iterations - 2):
            if(self.payoff_matrix[DEFECT][COOPERATE][0] > self.payoff_matrix[COOPERATE][COOPERATE][0]):
                return DEFECT
        
        #COOP on first round
        if self.round_counter == 1:
            return COOPERATE

        #special return for signal noise scenario
        if self.signal_noise > 0:
            noise_ret = self.play_noise()
            if(noise_ret != None):
                return noise_ret
        
        #return opponents last turn on other turns
        return self.opponent_moves[-1]

    #DEFECT. always
    def move_defect(self):
        '''Decide a move if the strategy is DEFECT, return bool'''
        #if the strategy is DEFECT it's always better to defect
        return DEFECT

    def move_alternate(self):
        '''Decide a move if the strategy is ALTERNATE, return bool'''
        #Always defect on last turn if WIN & DEFECT is better than LOSE
        if (self.number_of_iterations != 0) and (self.round_counter > self.number_of_iterations - 2):
            if(self.payoff_matrix[DEFECT][COOPERATE][0] > self.payoff_matrix[COOPERATE][DEFECT][0]) and (self.payoff_matrix[DEFECT][DEFECT][0] > self.payoff_matrix[COOPERATE][DEFECT][0]):
                return DEFECT
            else:
                return COOPERATE

        #for the first 5 rounds alternate
        if self.round_counter < 6:
            return self.round_counter % 2

        #analyze the result after 5 rounds
        if self.round_counter == 6:
            self.analyze_moves()
        
        #special return for signal noise scenario
        if self.signal_noise > 0:
            noise_ret = self.play_noise()
            if(noise_ret != None):
                return noise_ret

        return self.opponent_moves[-1]

    def move_always_coop(self):
        '''Always COOPERATE if it's the best move'''
        return COOPERATE

    
    def play_noise(self):
        '''Return special move to protect the decided game strategy in case of noise'''
        self.signal_noise -= 1
        if self.signal_noise > 0:
            return None
        
        #COOPERATE even if opponent DEFECTED last round
        if self.strategy == STRAT_COOP:
            return COOPERATE

        #If the strategy is alternate I expect opponent to repeat my moves
        #So return the opposite of my last move
        if self.strategy == STRAT_ALTERNATE:
            return (self.my_moves[-1] == False)
        
        return None


            
    def analyze_moves(self):
        '''Analyze the last few moves and change the strategy if necessary.'''
        #If opponent alternates as predicted, alternate
        if self.opponent_moves[-3:] == [COOPERATE, DEFECT, COOPERATE]:
            self.strategy = STRAT_ALTERNATE
        #if opponent always defects, always defect
        elif self.opponent_moves[-4:] == [DEFECT, DEFECT, DEFECT, DEFECT]:
            self.strategy = STRAT_DEFECT
        #if opponent always COOPs and win is better than coop always defect
        elif self.opponent_moves[-5:] == [COOPERATE, COOPERATE, COOPERATE , COOPERATE, COOPERATE]:
            if self.payoff_matrix[COOPERATE][COOPERATE][0] < self.payoff_matrix[DEFECT][COOPERATE][0]:
                self.strategy = STRAT_DEFECT

    def analyze_matrix(self, payoff_matrix):
        '''
        Analyze matrix for different strategies based on point income from two rounds.

        Arguments:\n
        payoff_matrix -- the payoff_matrix to analyze\n

        return value:\n
        1 -- COOP\n
        2 -- DEFECT\n
        3 -- ALTERNATE
        4 -- ALWAYS_COOP
        '''

        #if COOP better than ALTERNATE
        if(payoff_matrix[COOPERATE][COOPERATE][0] * 2) > (payoff_matrix[COOPERATE][DEFECT][0] + payoff_matrix[DEFECT][COOPERATE][0]):
            #if COOP better than DEFECT
            if (payoff_matrix[COOPERATE][COOPERATE][0] * 2) > (payoff_matrix[DEFECT][DEFECT][0] * 2):
                #if LOSE better than DEFECT
                if payoff_matrix[COOPERATE][DEFECT] > payoff_matrix[DEFECT][DEFECT]:
                    return STRAT_ALWAYS_COOP
                else:
                    return STRAT_COOP
            #if DEFECT better than COOP
            else:
                return STRAT_DEFECT
        #->ALTERNATE better than COOP

        #if DEFECT better than ALTERNATE
        if(payoff_matrix[DEFECT][DEFECT][0] * 2) > (payoff_matrix[COOPERATE][DEFECT][0] + payoff_matrix[DEFECT][COOPERATE][0]):
            return STRAT_DEFECT
        #-> ALTERNATE better than DEFECT
        return STRAT_ALTERNATE
            

if __name__ == "__main__":
    matrix = (((4,4),(2,6)),((6,1),(2,2)))
    p = MyPlayer(matrix)
    print(p.strategy)
    p.record_last_moves(False, True)
    p.record_last_moves(True, True)
    p.record_last_moves(False, True)
    p.record_last_moves(True, True)
    p.record_last_moves(False, True)
    p.round_counter = 5
    print(p.my_moves)
    print(p.opponent_moves)
    print(p.move())
    print(p.strategy)
    
    

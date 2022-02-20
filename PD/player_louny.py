COOPERATE = False
DEFECT = True

class MyPlayer:

    """
    Hráč vrací tah soupeře, poslední 2 tahy jsou True, první je False
    """
    def __init__(self, payoff, iter = -1):
        self.payoff = payoff
        self.iter = iter 
        self.opp_history = []
        self.my_history = []
        self.iter_num = 0
        self.strat = 1 
        
        
    def move(self):
        self.strat = self.analyze_payoff(self.payoff)
        if (self.strat == 1):
            output = self.strat_copycat()
            return output

        if (self.strat == 2):
            return COOPERATE

        if (self.strat == 3):
            return DEFECT
        
        if (self.strat == 4):
            output = self.strat_switch()
            return output
    
    def record_last_moves(self, my_move, opp_move):
        self.my_history.append(my_move)
        self.opp_history.append(opp_move)

    def analyze_payoff (self, payoff):
        output = 1
        payoff_matrix = payoff

        pm = {}
        pm["c","c"] = payoff_matrix[0][0]
        pm["d","d"] = payoff_matrix[1][1]
        pm["c","d"] = payoff_matrix[0][1]
        pm["d","c"] = payoff_matrix[1][0]

        my_coop = pm["c","c"][0]
        my_def = pm["d","d"][0]
        my_lose = pm["c","d"][0]
        my_win = pm["d","c"][0]

        coop_avg = (my_coop + my_lose) / 2.
        def_avg = (my_def + my_win) / 2.

        if ((my_win + my_lose) > (2 * my_coop) and (my_win + my_lose) > (2 * my_def)): 
                output = 4
        elif (def_avg > 2 * coop_avg):
                output = 3
        elif (my_coop > my_win and my_coop > my_def):
                output = 2

        return output

    def strat_copycat (self):
        self.iter_num += 1
        if (self.iter == -1):
                if (self.opp_cooperated()):
                        return COOPERATE
                if (self.opp_history != []):
                        return self.opp_history[-1]
                else:
                        return COOPERATE
        else:
                if (self.iter_num > self.iter -2):
                        return DEFECT
                if (self.opp_cooperated()):
                        return COOPERATE
                elif not(self.opp_history == []):
                        return self.opp_history[-1]
                else:
                        return COOPERATE

    def strat_switch(self):
        self.iter_num += 1
        if (self.iter_num == 1):
                return COOPERATE
        if (self.iter_num == 2):
                return DEFECT
        else:
                return self.opp_history[-1]

    def opp_cooperated(self):
        if (self.iter_num > 2):
                if (self.opp_history[-1] == DEFECT and self.opp_history[-2] == COOPERATE and self.opp_history[-3] == COOPERATE):
                        return True
                else:
                        return False
    



if __name__ == "__main__":
    p1 = MyPlayer(( ((4,4),(1,6)) , ((6,1),(2,2)) ), 10)

    for i in range(10):
        p1_move = p1.move()
        print(p1_move)
        p1.record_last_moves(False, True)
    
    print (p1.my_history)
    print (p1.opp_history)

    

 

    
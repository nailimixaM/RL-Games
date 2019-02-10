import numpy as np
import random
'''
Tic-tac-toe game.
Author: Max Croci
Date: 06.02.2019
'''

class Board:
    x_positions = []    #List of indices of "X" symbols
    o_positions = []    #List of indices of "O" symbols
    positions = {}      #Dictionary of symbols (values) at positions (keys) 1-9
    available_moves = []
    visited_states = []
    
    def __init__(self):
        self.x_positions = []
        self.o_positions = [] 
        self.available_moves = [i + 1 for i in range(9)] #List of possible moves 1-9
        self.positions = {}
        for i in range(9):
            self.positions[i+1] = "_"
        self.visited_states = []
        self.visited_states.append("_________")

    def print_board(self):
        row1 = ""
        row2 = ""
        row3 = ""
        for i in range(3):
            row1 += self.positions[1+i]
            row2 += self.positions[4+i]
            row3 += self.positions[7+i]
        print(row1)
        print(row2)
        print(row3)

    def update(self,move,symbol):
        self.positions[move] = symbol
        self.available_moves.remove(move)
        state = ""
        for i in range(9):
            state += self.positions[1+i]
        self.visited_states.append(state)

    def get_next_possible_states(self, symbol):
        cur_state = self.visited_states[-1]
        blank_pos = [pos for pos, char in enumerate(cur_state) if char == "_"]
        next_possible_states = {} #Dict keyed by moves, values are states
        for pos in blank_pos:
            if pos == 0:
                new_state = symbol + cur_state[1:9]
                next_possible_states[pos+1] = new_state
            elif pos == 8:
                new_state = cur_state[0:8] + symbol
                next_possible_states[pos+1] = new_state
            else:
                new_state = cur_state[0:pos] + symbol + cur_state[pos+1:9]
                next_possible_states[pos+1] = new_state

        return next_possible_states

    def check_victory(self, symbol):
        for i in range(1,4,1):
            if self.positions[3*i] != "_" and self.positions[3*i] ==  self.positions[3*i-1]\
                    and self.positions[3*i] == self.positions[3*i-2]:
                return True
            
            if self.positions[i] != "_" and self.positions[i] ==  self.positions[i+3]\
                    and self.positions[i] ==self.positions[i+6]:
                return True

        if self.positions[1] != "_" and self.positions[1] ==  self.positions[5]\
                and self.positions[1] == self.positions[9]:
            return True

        if self.positions[3] != "_" and self.positions[3] ==  self.positions[5]\
                and self.positions[5] == self.positions[7]:
            return True

        return False
 



class Bot:
    symbol = "" # "X" or "O"
    win = -1    # win = 1 if bot wins
    V = {}      # Estimated value of states (keys)
    num_wins = 0# Track number of bot wins

    def __init__(self,symbol,V,num_wins):
        self.symbol = symbol
        self.win = -1
        self.num_wins = num_wins
        self.V = V

    def get_move(self, board):
        next_possible_states = board.get_next_possible_states(self.symbol)
        candidate_moves = []
        candidate_V = []
        candidate_probabilities = []
        
        for poss_move, poss_state in next_possible_states.items():
            if poss_state not in self.V.keys():
                self.V[poss_state] = 0

            candidate_moves.append(poss_move)
            candidate_V.append(self.V[poss_state])

        tau = 1
        candidate_probabilities = list(np.exp(candidate_V)/sum(np.exp(candidate_V)))
        move = int(np.random.choice(candidate_moves,1,candidate_probabilities))
        #print("Move: " + str(move))
        return move



def main():
    print("Hello, welcome to tic-tac-toe!")
    
    ##Train the bots over many trials##
    MAX_NUM_TRIALS = 10000
    Vx = {}
    Vo = {}
    for n_trial in range(1,MAX_NUM_TRIALS+1,1):
        print("Trial: " + str(n_trial))
        board = Board()
        if n_trial == 1:
            bot1 = Bot("X",Vx,0)
            bot2 = Bot("O",Vo,0)
        else:
            bot1 = Bot("X",bot1.V,bot1.num_wins) #Load key bot variables from previous trial
            bot2 = Bot("O",bot2.V,bot2.num_wins) #Load key bot variables from previous trial

        bots = {}    
        bots[1] = bot1 
        bots[2] = bot2

        ##Run the game##
        MAX_NUM_TURNS = 9
        turn = 1
        victory = False
        while turn <= MAX_NUM_TURNS and not victory:
            bot = bots[2-(turn%2)]
            move = bot.get_move(board)
            board.update(move,bot.symbol)
            #board.print_board()
            victory = board.check_victory(bot.symbol)
            if (victory):
                bot.win = 1
                bot.num_wins = bot.num_wins + 1
                print("Player " + bot.symbol + " wins!")
            
            turn = turn + 1
            #print("#"*15)
        
        ##End of game: Update V using temporal-difference learning to train the bots##
        LEARN_RATE = 0.1
        REWARD = 100
        if victory:
            final_state = board.visited_states[-1]
            bot1.V[final_state] = REWARD*bot1.win
            bot2.V[final_state] = REWARD*bot2.win 
        else:
            final_state = board.visited_states[-1]
            bot1.V[final_state] = 0
            bot2.V[final_state] = 0 

        for state in board.visited_states:
            if state not in bot1.V:
                bot1.V[state] = 0
            if state not in bot2.V:
                bot2.V[state] = 0

        n_states_visited = len(board.visited_states)
        for i in range(n_states_visited-1):
            state = board.visited_states[n_states_visited -i -2]
            next_state = board.visited_states[n_states_visited -i -1]
            bot1.V[state] = bot1.V[state] + LEARN_RATE*(bot1.V[next_state] - bot1.V[state])
            bot2.V[state] = bot2.V[state] + LEARN_RATE*(bot2.V[next_state] - bot2.V[state])

    ##Analyse results#
    print(len(bot1.V))
    print(len(bot2.V))
    print(bot1.num_wins)
    print(bot2.num_wins)

if __name__ == "__main__":
    main()

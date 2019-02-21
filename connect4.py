import numpy as np
import random
import matplotlib.pyplot as plt
'''
Connect 3 game.
Author: Max Croci
Date: 21.02.2019
'''

class Board:
    x_positions = []    #List of indices of "X" symbols
    o_positions = []    #List of indices of "O" symbols
    positions = {}      #Dictionary of symbols (values) at positions (keys) 1-16
    available_moves = []#List of available moves
    visited_states = [] #List of visited states
    
    def __init__(self):
        self.x_positions = []
        self.o_positions = [] 
        self.available_moves = [i + 1 for i in range(4)] #List of possible moves 1-4
        self.positions = {}
        for i in range(16):
            self.positions[i+1] = "_"
        self.visited_states = []
        self.visited_states.append("_"*16)

    def print_board(self):
        row1 = ""
        row2 = ""
        row3 = ""
        row4 = ""
        for i in range(3):
            row1 += self.positions[1+i]
            row2 += self.positions[4+i]
            row3 += self.positions[7+i]
            row4 += self.positions[10+i]
        print(row1)
        print(row2)
        print(row3)
        print(row4)

    def update(self,move,symbol):
        cur_state = self.visited_states[-1]
        if cur_state[move+11] == "_":
            self.positions[move+12] = symbol
        elif cur_state[move+7] == "_":
            self.positions[move+8] = symbol
        elif cur_state[move+3] == "_":
            self.positions[move+4] = symbol
        elif cur_state[move-1] == "_":
            self.positions[move] = symbol
        
        state = ""
        for i in range(16):
            state += self.positions[1+i]
        self.visited_states.append(state)

    def get_next_possible_states(self, symbol):
        cur_state = self.visited_states[-1]
        moves = self.available_moves
        next_possible_states = {} #Dict keyed by moves, values are states
        for move in moves:
            if cur_state[move+11] == "_":
                new_state = cur_state[:move+11] + symbol + cur_state[move+12:]
                next_possible_states[move] = new_state
            elif cur_state[move+7] == "_":
                new_state = cur_state[:move+7] + symbol + cur_state[move+8:]
                next_possible_states[move] = new_state
            elif cur_state[move+3] == "_":
                new_state = cur_state[:move+3] + symbol + cur_state[move+4:]
                next_possible_states[move] = new_state
            elif cur_state[move-1] == "_":
                new_state = cur_state[:move-1] + symbol + cur_state[move:]
                next_possible_states[move] = new_state
            else:
                print("Warning: " + str(move) + " is invalid")

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
    tau = 0     #"Heat" controls exploration v exploitation
    training = True

    def __init__(self,symbol,V,num_wins,tau,training):
        self.symbol = symbol
        self.win = -1
        self.num_wins = num_wins
        self.V = V
        self.tau = tau
        self.training = training
    
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

        if self.training:
            candidate_V[:] = [x/self.tau for x in candidate_V]
            candidate_probabilities = list(np.exp(candidate_V)/sum(np.exp(candidate_V)))
            move = int(np.random.choice(candidate_moves,1,candidate_probabilities))
        
        else:
            max_V = max(candidate_V)
            possible_moves = [candidate_moves[i] for i,j in enumerate(candidate_V) if j == max_V]
            move = np.random.choice(possible_moves)

        return move


def main():
    print("Hello, welcome to connect3!")
    
    board = Board()
    board.print_board()
    nps = board.get_next_possible_states("X")
    print(nps)
    board.update(1,"X")
    print(board.positions)
    print(board.visited_states)

if __name__ == "__main__":
    main()

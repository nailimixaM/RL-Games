import numpy as np
import random
import matplotlib.pyplot as plt
'''
Connect 3 game.
Author: Max Croci
Date: 21.02.2019
'''

class Board:
    positions = {}      #Dictionary of symbols (values) at positions (keys) 1-16
    available_moves = []#List of available moves
    visited_states = [] #List of visited states
    filled_positions =[]#List of positions filled from chosen moves
    chosen_moves = []   #List of moves that have been made

    def __init__(self):
        self.available_moves = [i + 1 for i in range(4)] #List of possible moves 1-4
        self.positions = {}
        for i in range(16):
            self.positions[i+1] = "_"
        self.visited_states = []
        self.visited_states.append("_"*16)
        self.filled_positions = []
        self.chosen_moves = []

    def print_board(self):
        row1 = ""
        row2 = ""
        row3 = ""
        row4 = ""
        for i in range(4):
            row1 += self.positions[1+i]
            row2 += self.positions[5+i]
            row3 += self.positions[9+i]
            row4 += self.positions[13+i]
        print(row1)
        print(row2)
        print(row3)
        print(row4)
    
    def move_to_position(self,move): 
        cur_state = self.visited_states[-1]
        if cur_state[move+11] == "_":
            position = move+12
        elif cur_state[move+7] == "_":
            position = move+8
        elif cur_state[move+3] == "_":
            position = move+4
        elif cur_state[move-1] == "_":
            position = move

        print("Move " + str(move) + " equiv to position " + str(position)) 
        self.filled_positions.append(position)
        self.chosen_moves.append(move)
        return position

    def update(self,move,symbol):
        position = self.move_to_position(move)
        self.positions[position] = symbol

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
            #else:
                #print("Warning: " + str(move) + " is invalid")

        return next_possible_states

    def check_victory(self, symbol):
        last_filled_pos = self.filled_positions[-1] #Only need to check for win around last position
        last_move = self.chosen_moves[-1]
        last_move_row = int(np.floor(1+(last_filled_pos-1)/4))

        if last_filled_pos <= 8: #Check vertical if in top two rows
            if self.positions[last_filled_pos] == self.positions[last_filled_pos+4]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos+8]: 
                print("Game is won vertically!")
                return True
        
        if last_move == 1: 
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos+1]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos+2]: 
                print("Win horizontally!")
                return True
        
        elif last_move == 4:
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos-1]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos-2]: 
                print("Win horizontally!")
                return True

        elif last_move == 2:
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos+1]:
                if self.positions[last_filled_pos] == self.positions[last_filled_pos+2]:
                    return True              
                elif self.positions[last_filled_pos] == self.positions[last_filled_pos-1]:
                    return True              
        
        elif last_move == 3:
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos-1]:
                if self.positions[last_filled_pos] == self.positions[last_filled_pos-2]:
                    return True              
                elif self.positions[last_filled_pos] == self.positions[last_filled_pos+1]:
                    return True              
                

        return False
 

class Bot:
    symbol = "" # "X" or "O"
    win = -1    # win = 1 if bot wins
    V = {}      # Estimated value of states (keys)
    num_wins = 0# Track number of bot wins
    tau = 1     #"Heat" controls exploration v exploitation
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
    bot1 = Bot("X",{},0,1,True)
    bot2 = Bot("O",{},0,1,True)
    
    bots = {}
    bots[1] = bot1
    bots[2] = bot2
    
    ##Run the game##
    MAX_NUM_TURNS = 16
    turn = 1
    victory = False

    while turn <= MAX_NUM_TURNS and not victory:
        bot = bots[2-(turn%2)]
        move = bot.get_move(board)
        board.update(move,bot.symbol)
        board.print_board()
        victory = board.check_victory(bot.symbol)
        
        turn = turn + 1
        print("#"*15)

if __name__ == "__main__":
    main()

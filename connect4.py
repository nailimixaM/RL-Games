import numpy as np
import random
import matplotlib.pyplot as plt
import os
'''
Connect 4 game.
Author: Max Croci
Date: 2.Mar.2019
'''

class Board:
    positions = {}      #Dictionary of symbols (values) at positions (keys) 1-42
    available_moves = []#List of available moves
    visited_states = [] #List of visited states
    filled_positions =[]#List of positions filled from chosen moves
    chosen_moves = []   #List of moves that have been made

    def __init__(self):
        self.available_moves = [i + 1 for i in range(7)] #List of possible moves 1-7
        self.positions = {}
        for i in range(42):
            self.positions[i+1] = "_"
        self.visited_states = []
        self.visited_states.append("_"*42)
        self.filled_positions = []
        self.chosen_moves = []

    def print_board(self):
        row1 = ""
        row2 = ""
        row3 = ""
        row4 = ""
        row5 = ""
        row6 = ""
        for i in range(7):
            row1 += self.positions[1+i]
            row2 += self.positions[8+i]
            row3 += self.positions[15+i]
            row4 += self.positions[22+i]
            row5 += self.positions[29+i]
            row6 += self.positions[36+i]
        print(row1)
        print(row2)
        print(row3)
        print(row4)
        print(row5)
        print(row6)
    
    def move_to_position(self,move): 
        cur_state = self.visited_states[-1]
        if cur_state[move+34] == "_":
            position = move+35
        elif cur_state[move+27] == "_":
            position = move+28
        elif cur_state[move+20] == "_":
            position = move+21
        elif cur_state[move+13] == "_":
            position = move+14
        elif cur_state[move+6] == "_":
            position = move+7
        elif cur_state[move-1] == "_":
            position = move

        #print("Move " + str(move) + " equiv to position " + str(position)) 
        self.filled_positions.append(position)
        self.chosen_moves.append(move)
        return position

    def update(self,move,symbol):
        position = self.move_to_position(move)
        self.positions[position] = symbol

        state = ""
        for i in range(42):
            state += self.positions[1+i]
        self.visited_states.append(state)

    def get_next_possible_states(self, symbol):
        cur_state = self.visited_states[-1]
        moves = self.available_moves
        next_possible_states = {} #Dict keyed by moves, values are states
        for move in moves:
            if cur_state[move+34] == "_":
                new_state = cur_state[:move+34] + symbol + cur_state[move+35:]
                next_possible_states[move] = new_state
            elif cur_state[move+27] == "_":
                new_state = cur_state[:move+27] + symbol + cur_state[move+28:]
                next_possible_states[move] = new_state
            elif cur_state[move+20] == "_":
                new_state = cur_state[:move+20] + symbol + cur_state[move+21:]
                next_possible_states[move] = new_state
            elif cur_state[move+13] == "_":
                new_state = cur_state[:move+13] + symbol + cur_state[move+14:]
                next_possible_states[move] = new_state
            elif cur_state[move+6] == "_":
                new_state = cur_state[:move+6] + symbol + cur_state[move+7:]
                next_possible_states[move] = new_state
            elif cur_state[move-1] == "_":
                new_state = cur_state[:move-1] + symbol + cur_state[move:]
                next_possible_states[move] = new_state

        return next_possible_states

    def check_victory(self, symbol):
        last_filled_pos = self.filled_positions[-1] #Only need to check for win around last position
        last_move = self.chosen_moves[-1]
        last_move_row = int(np.floor(1+(last_filled_pos-1)/7))
        last_move_col = (last_filled_pos-1)%7 + 1

        if last_filled_pos <= 21: #Check vertical if in top two rows
            if self.positions[last_filled_pos] == self.positions[last_filled_pos+7]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos+14]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos+21]: 
                #print("Game is won vertically!")
                return True
        
        for i in range (1,5): #check horizontal
            if self.positions[i+(last_move_row-1)*7] != "_"\
                    and self.positions[i+(last_move_row-1)*7] == self.positions[i+1+(last_move_row-1)*7]\
                    and self.positions[i+(last_move_row-1)*7] == self.positions[i+2+(last_move_row-1)*7]\
                    and self.positions[i+(last_move_row-1)*7] == self.positions[i+3+(last_move_row-1)*7]: 
                #print("Win horizontally!")
                return True 

        #Check diagonals
        itmp = [1, 2, 3, 4, 8, 9, 10, 11, 15, 16, 17, 18]
        istarts = [i for i in itmp if i in self.filled_positions]
        for i in istarts:
            if self.positions[i] == self.positions[i+8]\
                    and self.positions[i] == self.positions[i+16]\
                    and self.positions[i] == self.positions[i+24]:
                #print("Win -ve diag")
                return True

        itmp = [4, 5, 6, 7, 11, 12, 13, 14, 18, 19, 20, 21]
        istarts = [i for i in itmp if i in self.filled_positions]
        for i in istarts:
            if self.positions[i] == self.positions[i+6]\
                    and self.positions[i] == self.positions[i+12]\
                    and self.positions[i] == self.positions[i+18]:
                #print("Win +ve diag")
                return True
        return False 


class Bot:
    symbol = "" # "X" or "O"
    win = 0   # win = 1 if bot wins
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

    def update_V(self,board,REWARD,LEARN_RATE):
        final_state = board.visited_states[-1]
        self.V[final_state] = REWARD*self.win
        for state in board.visited_states:
            if state not in self.V:
                self.V[state] = 0

        n_states_visited = len(board.visited_states)
        for i in range(n_states_visited-1):
            state = board.visited_states[n_states_visited -i -2]
            next_state = board.visited_states[n_states_visited -i -1]
            self.V[state] = self.V[state] + LEARN_RATE*(self.V[next_state] - self.V[state])

        #Mirror states - make use of symmetry
        mirror_visited_states = []
        for state in board.visited_states:
            mirror_row1 = state[0:7]
            mirror_row2 = state[7:14]
            mirror_row3 = state[14:21]
            mirror_row4 = state[21:28]
            mirror_row5 = state[28:35]
            mirror_row6 = state[35:42]
            mirror_state = mirror_row1[::-1] + mirror_row2[::-1] + mirror_row3[::-1] \
                    + mirror_row4[::-1] + mirror_row5[::-1] + mirror_row6[::-1]
            self.V[mirror_state] = self.V[state]
            '''
            mirror_visited_states.append(mirror_state)
        
        final_state = mirror_visited_states[-1]
        self.V[final_state] = REWARD*self.win
        for state in mirror_visited_states:
            if state not in self.V:
                self.V[state] = 0

        for i in range(n_states_visited-1):
            state = mirror_visited_states[n_states_visited -i -2]
            next_state = mirror_visited_states[n_states_visited -i -1]
            if state not in board.visited_states: #Do not update symmetrical positions twice
                self.V[state] = self.V[state] + LEARN_RATE*(self.V[next_state] - self.V[state])
            '''

def main():
    print("Hello, welcome to connect3!")
    
    ##Train the bots over many trials##
    print("Please enter the number of trials (games) to train the bots over (10k trials takes approx 20s): ")
    MAX_NUM_TRIALS = input()
    while MAX_NUM_TRIALS.isdigit() == False:
        print("Error, please try again:")
        MAX_NUM_TRIALS = input()
    MAX_NUM_TRIALS = int(MAX_NUM_TRIALS)

    tau = 20
    for n_trial in range(1,MAX_NUM_TRIALS+1,1):
        #print("#"*15)
        if n_trial%1000 == 0:
            print("Trial: " + str(n_trial) + " of " + str(MAX_NUM_TRIALS))
        if n_trial%5000 == 0:
            tau = tau/2

        if n_trial == 1:
            bot1 = Bot("X",{},0,tau,True)
            bot2 = Bot("O",{},0,tau,True)
        else:
            bot1 = Bot("X",bot1.V,bot1.num_wins,tau,True) #Load key bot variables from previous trial
            bot2 = Bot("O",bot2.V,bot2.num_wins,tau,True) #Load key bot variables from previous trial

        bots = {}
        bots[1] = bot1
        bots[2] = bot2
        board = Board()
 
        ##Run the game##
        MAX_NUM_TURNS = 42
        REWARD = 100
        LEARN_RATE = 0.25
        turn = 1
        victory = False

        while turn <= MAX_NUM_TURNS and not victory:
            bot = bots[2-(turn%2)]
            move = bot.get_move(board)
            board.update(move,bot.symbol)
            #board.print_board()

            victory = board.check_victory(bot.symbol)
            if victory:
                bot.win = 1
                bot.num_wins = bot.num_wins + 1
                #print("Bot " + bot.symbol + " wins!")

            turn = turn + 1
            #print("#"*15)
      
        ##Update bots
        for botnum,bot in bots.items():
            if victory and bot.win == 0:
                bot.win = -1
            bot.update_V(board,REWARD,LEARN_RATE)

    ##Analyse training results##
    print("Training complete!")
    print("X won " + str(bot1.num_wins) + " games and analysed " + str(len(bot1.V)) + " positions.")
    print("O won " + str(bot2.num_wins) + " games and analysed " + str(len(bot2.V)) + " positions.") 
    save_results(bot1,bot2,MAX_NUM_TRIALS,"trials")
    
    ##Test the bots against each other aggressively##
    print("Please enter the number of tests: ")
    MAX_NUM_TESTS = input()
    while MAX_NUM_TESTS.isdigit() == False:
        print("Error, please try again:")
        MAX_NUM_TESTS = input()
    MAX_NUM_TESTS = int(MAX_NUM_TESTS)

    for n_trial in range(1,MAX_NUM_TESTS+1,1):
        #print("#"*15)
        if n_trial%1000 == 0:
            print("Test: " + str(n_trial) + " of " + str(MAX_NUM_TRIALS))

        if n_trial == 1:
            bot1 = Bot("X",bot1.V,0,0,False)
            bot2 = Bot("O",bot2.V,0,0,False)
        else:
            bot1 = Bot("X",bot1.V,bot1.num_wins,0,False) #Load key bot variables from previous trial
            bot2 = Bot("O",bot2.V,bot2.num_wins,0,False) #Load key bot variables from previous trial

        bots = {}
        bots[1] = bot1
        bots[2] = bot2
        board = Board()
 
        ##Run the game##
        MAX_NUM_TURNS = 16
        REWARD = 100
        LEARN_RATE = 0.1
        turn = 1
        victory = False

        while turn <= MAX_NUM_TURNS and not victory:
            bot = bots[2-(turn%2)]
            move = bot.get_move(board)
            board.update(move,bot.symbol)
            #board.print_board()
            victory = board.check_victory(bot.symbol)
            if victory:
                bot.win = 1
                bot.num_wins = bot.num_wins + 1
                print("Bot " + bot.symbol + " wins!")

            turn = turn + 1
            #print("#"*15)
      
        ##Update bots
        for botnum,bot in bots.items():
            if victory and bot.win == 0:
                bot.win = -1
            bot.update_V(board,REWARD,LEARN_RATE)

    ##Analyse testing results##
    print("Testing complete!")
    print("X won " + str(bot1.num_wins) + " games and analysed " + str(len(bot1.V)) + " positions.")
    print("O won " + str(bot2.num_wins) + " games and analysed " + str(len(bot2.V)) + " positions.")

    save_results(bot1,bot2,MAX_NUM_TESTS,"tests")

def save_results(bot1,bot2,MAX_NUM,case):
    path = os.getcwd() + os.sep
    res_dir = "connect4results" + os.sep
    res_path = path + res_dir
    if not os.path.exists(res_path):
        os.mkdir(res_path)

    filename = res_dir + "results_" + str(MAX_NUM) + "_" + case + ".txt"
    f = open(filename,"w")
    state_msg = "X analysed " + str(len(bot1.V)) + " states, O analysed " + str(len(bot2.V)) + ".\n"

    for state, value in bot1.V.items():
        if state not in bot2.V:
            bot2.V[state] = 0

    for state, value in bot2.V.items():
        if state not in bot1.V:
            bot1.V[state] = 0

    if case == "trials":
        f.write("Results of training with " + str(MAX_NUM) + " trials.\n")
    else:
        f.write("Results of testing with " + str(MAX_NUM) + " tests.\n")

    res_msg = "X won " + str(bot1.num_wins) + " games, O won " + str(bot2.num_wins) + ".\n"
    f.write(res_msg)
    f.write(state_msg)
    f.write("#"*len(state_msg) + "\n")
    f.write("State values V(s) estimated by X and O:\n")

    for state, value in bot1.V.items():
        f.write("-"*len(state_msg) + "\n")
        f.write(state[0:7] + "\n")
        f.write(state[7:14] +"\n")
        f.write(state[14:21] + " "*4 + "V(s) for X: " + str(round(value,3))  + "\n")
        f.write(state[21:28] + " "*4 + "V(s) for O: " + str(round(bot2.V[state],3))  + "\n")
        f.write(state[28:35] + "\n")
        f.write(state[35:42] + "\n")




if __name__ == "__main__":
    main()

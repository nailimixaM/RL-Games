import numpy as np
import random
import matplotlib.pyplot as plt
import os
'''
Connect 3 game.
Author: Max Croci
Date: 21.02.2019
'''

class Board:
    n_rows = 0
    n_cols = 0
    positions = {}      #Dictionary of symbols (values) at positions (keys)
    available_moves = []#List of available moves
    visited_states = [] #List of visited states
    filled_positions =[]#List of positions filled from chosen moves
    chosen_moves = []   #List of moves that have been made

    def __init__(self,variant):
        self.positions = {}
        self.visited_states = []
        self.filled_positions = []
        self.chosen_moves = []
        if variant == 3:
            self.n_rows = 4
            self.n_cols = 4
        elif variant == 4:
            self.n_rows = 6
            self.n_cols = 7

        self.available_moves = [i + 1 for i in range(self.n_cols)]
        for i in range(self.n_rows*self.n_cols):
            self.positions[i+1] = "_"
        self.visited_states.append("_"*self.n_rows*self.n_cols)

    def print_board(self):
        for i in range(self.n_rows):
            row = ""
            for j in range(self.n_cols):
                row += self.positions[1+self.n_cols*i+j]
            print(row)
    
    def move_to_position(self,move): 
        cur_state = self.visited_states[-1]
        for i in range(self.n_rows-1,-1,-1):
            if cur_state[move+i*self.n_cols-1] == "_":
                position = move+i*self.n_cols
                self.filled_positions.append(position)
                self.chosen_moves.append(move)
                print("Move " + str(move) + " equiv to position " + str(position)) 
                return position

    def update(self,move,symbol):
        position = self.move_to_position(move)
        self.positions[position] = symbol
        if position <= self.n_cols:
            self.available_moves.remove(move)

        state = ""
        for i in range(self.n_rows*self.n_cols):
            state += self.positions[1+i]
        
        self.visited_states.append(state)

    def get_next_possible_states(self, symbol):
        cur_state = self.visited_states[-1]
        print(cur_state)
        moves = self.available_moves
        next_possible_states = {} #Dict keyed by moves, values are states
        for move in moves:
            for i in range(self.n_rows-1,-1,-1):
                if move not in next_possible_states:
                    if cur_state[move+i*self.n_cols-1] == "_":
                        new_state = cur_state[:move+i*self.n_cols-1]\
                                + symbol\
                                + cur_state[move+i*self.n_cols:]
                        next_possible_states[move] = new_state
        
        return next_possible_states

    def check_victory(self, symbol):
        last_filled_pos = self.filled_positions[-1] #Only need to check for win around last position
        last_move = self.chosen_moves[-1]
        last_move_row = int(np.floor(1+(last_filled_pos-1)/4))
        last_move_col = (last_filled_pos-1)%4 + 1

        if last_filled_pos <= 8: #Check vertical if in top two rows
            if self.positions[last_filled_pos] == self.positions[last_filled_pos+4]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos+8]: 
                #print("Game is won vertically!")
                return True
        
        if last_move == 1: 
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos+1]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos+2]: 
                #print("Win horizontally!")
                return True
        
        elif last_move == 4:
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos-1]\
                    and self.positions[last_filled_pos] == self.positions[last_filled_pos-2]: 
                #print("Win horizontally!")
                return True

        elif last_move == 2:
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos+1]:
                if self.positions[last_filled_pos] == self.positions[last_filled_pos+2]:
                    #print("Win horizontally!")
                    return True              
                elif self.positions[last_filled_pos] == self.positions[last_filled_pos-1]:
                    #print("Win horizontally!")
                    return True              
        
        elif last_move == 3:
            #check horizontal
            if self.positions[last_filled_pos] == self.positions[last_filled_pos-1]:
                if self.positions[last_filled_pos] == self.positions[last_filled_pos-2]:
                    #print("Win horizontally!")
                    return True              
                elif self.positions[last_filled_pos] == self.positions[last_filled_pos+1]:
                    #print("Win horizontally!")
                    return True              
        
        #Check diagonals
        itmp = [1, 2, 5, 6]
        istarts = [i for i in itmp if i in self.filled_positions]
        for i in istarts:
            if self.positions[i] == self.positions[i+5]\
                    and self.positions[i] == self.positions[i+10]:
                #print("Win -ve diag")
                return True

        itmp = [3, 4, 7, 8]
        istarts = [i for i in itmp if i in self.filled_positions]
        for i in istarts:
            if self.positions[i] == self.positions[i+3]\
                    and self.positions[i] == self.positions[i+6]:
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
            mirror_row1 = state[0:4]
            mirror_row2 = state[4:8]
            mirror_row3 = state[8:12]
            mirror_row4 = state[12:16]
            mirror_state = mirror_row1[::-1] + mirror_row2[::-1] + mirror_row3[::-1] + mirror_row4[::-1]
            self.V[mirror_state] = self.V[state]


def main():
    print("Hello, welcome to connectX!")

    valid_variant = False
    while not valid_variant:
        print("Which variant would you like to play? Type '3' for Connect3 or '4' for Connect4:")
        variant = input()
        if variant is "3":
            valid_variant = True
        elif variant is "4":
            valid_variant = True
        else:
            print("I'm sorry, " + variant + " isn't a valid option, please try again.")
   
    variant = int(variant)
    quit = False
    while not quit:
        print("Would you like to train, test or play against a bot? Type 'r' to train, 'e' to test,'p' to play or 'q' to quit:")
        ans = input()
        if ans is "r":
            train_bots(variant)
            print('\n')
        elif ans is "e":
            test_bots(variant)
            print('\n')
        elif ans is "p":
            play_bot(variant)
            print('\n')
        elif ans is "q":
            quit = True
            print("Goodbye!")
        else:
            print("I'm sorry, " + ans + " isn't a valid option, please try again.")

def train_bots(variant):
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
        board = Board(variant)
 
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

def test_bots(variant):
    ##Load V from a file saved through training process##
    print("The following saved bots exist: ")
    num_bots = 0
    for f in os.listdir("connect3results" + os.sep):
        if f[0] == "V":
            num_bots = num_bots + 1
            print("#" + str(num_bots) + ": " + f)
    
    if num_bots == 0:
        print("No saved bots found! Please train a bot before testing it.")
        return -1
    
    print("Type a number eg '1' to choose the bot:")
    bot_chosen = int(input())
    num_bots = 0
    for f in os.listdir("connect3results" + os.sep):
        if f[0] == "V":
            num_bots = num_bots + 1
            if bot_chosen == num_bots:
                [Vx, Vo] = read_V_file(f)

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
            print("Test: " + str(n_trial) + " of " + str(MAX_NUM_TESTS))

        if n_trial == 1:
            bot1 = Bot("X",Vx,0,0,False)
            bot2 = Bot("O",Vo,0,0,False)
        else:
            bot1 = Bot("X",bot1.V,bot1.num_wins,0,False) #Load key bot variables from previous trial
            bot2 = Bot("O",bot2.V,bot2.num_wins,0,False) #Load key bot variables from previous trial

        bots = {}
        bots[1] = bot1
        bots[2] = bot2
        board = Board(variant)
 
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
                #print("Bot " + bot.symbol + " wins!")

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

def play_bot(variant):
    ##Load V from a file saved through training process##
    print("The following saved bots exist: ")
    num_bots = 0
    for f in os.listdir("connect3results" + os.sep):
        if f[0] == "V":
            num_bots = num_bots + 1
            print("#" + str(num_bots) + ": " + f)

    print("Type a number eg '1' to choose the bot:")
    bot_chosen = int(input())
    num_bots = 0
    for f in os.listdir("connect3results" + os.sep):
        if f[0] == "V":
            num_bots = num_bots + 1
            if bot_chosen == num_bots:
                [Vx, Vo] = read_V_file(f)

    play_game = True
    while play_game:
        board = Board(variant)
        print("Play as player '1' or '2'?")
        valid_answer = False
        while not valid_answer:
            answer = input()
            if answer == "1" or answer == "2":
                player = int(answer)
                valid_answer = True
            else:
                print("Error, please enter '1' or '2'")

        if player == 1:
            player_symbol = "X"
            bot = Bot("O",Vo,0,0,False)
        else:
            bot = Bot("X",Vx,0,0,False)
            player_symbol = "O"


        ##Run the game##
        MAX_NUM_TURNS = 42
        turn = 1
        victory = False
        board.print_board()
        while turn <= MAX_NUM_TURNS and not victory:
            cur_player = (turn-1)%2 + 1
            if cur_player == player:
                print("Please make a move. Available moves:")
                print(board.available_moves)
                move = int(input())
                while move not in board.available_moves:
                    print("Error: move unavailable. Available moves:")
                    print(board.available_moves)
                    move = int(input())
                board.update(move,player_symbol)
            else:
                n_states = board.get_next_possible_states(bot.symbol)
                for mov, state in n_states.items():
                    if state in bot.V:
                        print("State " + state + " has value: " + str(bot.V[state]))
                    else:
                        print("State " + state + " not analysed yet.")

                move = bot.get_move(board)
                board.update(move,bot.symbol)

            print("#"*15)
            board.print_board()
            victory = board.check_victory(bot.symbol)
            if (victory):
                if cur_player == player:
                    print("Game over: you win!")
                else:
                    print("Game over: you lose!")

            turn = turn + 1

        print("Would you like to play again? (y/n)")
        valid_answer = False
        while not valid_answer:
            answer = input()
            if answer == "y":
                play_game = True
                valid_answer = True
            elif answer == "n":
                play_game = False
                valid_answer = True
                print("Goodbye!")
            else:
                print("Error, please enter 'y' or 'n':")

def read_V_file(filename):
    Vx = {}
    Vo = {}
    res_dir = "connect3results" + os.sep
    f = open(res_dir + filename,'r')
    num_lines = 0
    for line in f:
        num_lines = num_lines + 1
        if num_lines%100000 == 0:
            print("Loaded " + str(num_lines) + " lines...")
        state, value = line.rstrip('\n').split('\t')
        Vx[state] = float(value)
        Vo[state] = -float(value)
    V = [Vx, Vo]
    return V

def save_results(bot1,bot2,MAX_NUM,case):
    path = os.getcwd() + os.sep
    res_dir = "connect3results" + os.sep
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
        f.write(state[0:4] + " "*4 + "V(s) for X: " + str(round(value,3)) + "\n")
        f.write(state[4:8] + " "*4 + "V(s) for O: " + str(round(bot2.V[state],3)) +"\n")
        f.write(state[8:12] + "\n")
        f.write(state[12:16] + "\n")
    f.close()

    filename = res_dir + "V_" + str(MAX_NUM) + "_" + case + ".txt"
    f = open(filename,"w")
    for state, value in bot1.V.items():
        f.write(state + "\t" + str(value) + "\n")
    f.close()




if __name__ == "__main__":
    main()

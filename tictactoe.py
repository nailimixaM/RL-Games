import numpy as np
import random
import matplotlib.pyplot as plt
import os
'''
Tic-tac-toe game.
Author: Max Croci
Date: 06.02.2019
'''

class Board:
    x_positions = []    #List of indices of "X" symbols
    o_positions = []    #List of indices of "O" symbols
    positions = {}      #Dictionary of symbols (values) at positions (keys) 1-9
    available_moves = []#List of available moves
    visited_states = [] #List of visited states
    
    def __init__(self):
        self.x_positions = []
        self.o_positions = [] 
        self.available_moves = [i + 1 for i in range(9)] #List of possible moves 1-9
        self.positions = {}
        for i in range(9):
            self.positions[i+1] = "_"
        self.visited_states = []
        self.visited_states.append("_"*9)

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
    print("Hello, welcome to tic-tac-toe!")
    print("Please enter the number of trials (games) to train the bots over (10k trials takes approx 20s): ")
    MAX_NUM_TRIALS = input()
    while MAX_NUM_TRIALS.isdigit() == False:
        print("Error, please try again:")
        MAX_NUM_TRIALS = input()
    MAX_NUM_TRIALS = int(MAX_NUM_TRIALS)
    
    print("Please enter the number of tests (games) to test the bots over (10k tests takes approx 15s): ") 
    MAX_NUM_TESTS = input()
    while MAX_NUM_TESTS.isdigit() == False:
        print("Error, please try again:")
        MAX_NUM_TESTS = input()
    MAX_NUM_TESTS = int(MAX_NUM_TESTS)
    
    tau = 20

    ##Train the bots over many trials##
    for n_trial in range(1,MAX_NUM_TRIALS+1,1):
        print("Trial: " + str(n_trial) + " of " + str(MAX_NUM_TRIALS))
        if n_trial%5000 == 0:
            tau = tau/2

        board = Board()
        if n_trial == 1:
            bot1 = Bot("X",{},0,tau,True)
            bot2 = Bot("O",{},0,tau,True)
        else:
            bot1 = Bot("X",bot1.V,bot1.num_wins,tau,True) #Load key bot variables from previous trial
            bot2 = Bot("O",bot2.V,bot2.num_wins,tau,True) #Load key bot variables from previous trial

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
    
    ##Analyse training results##
    print("Training complete!")
    print("X won " + str(bot1.num_wins) + " games and analysed " + str(len(bot1.V)) + " positions.")
    print("O won " + str(bot2.num_wins) + " games and analysed " + str(len(bot2.V)) + " positions.")
    save_results(bot1,bot2,MAX_NUM_TRIALS,"trials")

    ##Bots play each other aggressively##

    Xwins = []
    Owins = []
    Draws = []
    Draws.append(0)
    for n_test in range(1,MAX_NUM_TESTS+1,1):
        print("Test: " + str(n_test) + " of " + str(MAX_NUM_TESTS))
        if n_test == 1:
            bot1 = Bot("X",bot1.V,0,0,False) #Load key bot variables from previous trial
            bot2 = Bot("O",bot2.V,0,0,False) #Load key bot variables from previous trial
        else:
            bot1 = Bot("X",bot1.V,bot1.num_wins,0,False) #Load key bot variables from previous trial
            bot2 = Bot("O",bot2.V,bot2.num_wins,0,False) #Load key bot variables from previous trial
        
        bots = {}    
        bots[1] = bot1 
        bots[2] = bot2
        board = Board()

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
        Xwins.append(bot1.num_wins)
        Owins.append(bot2.num_wins)
        LEARN_RATE = 0.1
        REWARD = 100
        if victory:
            final_state = board.visited_states[-1]
            bot1.V[final_state] = REWARD*bot1.win
            bot2.V[final_state] = REWARD*bot2.win 
            Draws.append(Draws[-1])

        else:
            final_state = board.visited_states[-1]
            bot1.V[final_state] = 0
            bot2.V[final_state] = 0
            Draws.append(Draws[-1]+1)

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
    
    ##Analyse test results##
    print("Testing complete!")
    print("X won " + str(bot1.num_wins) + " games and analysed " + str(len(bot1.V)) + " positions.")
    print("O won " + str(bot2.num_wins) + " games and analysed " + str(len(bot2.V)) + " positions.")
    save_results(bot1,bot2,MAX_NUM_TESTS,"tests")
    xx = [i+1 for i in range(MAX_NUM_TESTS)]
    Xwins = [100*xwin/x for xwin,x in zip(Xwins[:MAX_NUM_TESTS],xx)] 
    Owins = [100*owin/x for owin,x in zip(Owins[:MAX_NUM_TESTS],xx)] 
    Draws = [100*draw/x for draw,x in zip(Draws[1:MAX_NUM_TESTS+1],xx)] 
    plt.scatter(xx,Xwins,label = 'X wins')
    plt.scatter(xx,Owins,label = 'O wins')
    plt.scatter(xx,Draws,label = 'Draws')
    plt.title("Bot v Bot test results")
    plt.xlabel("Number of test games")
    plt.ylabel("%")
    plt.legend()
    plt.show()

    ##Play bot##
    print("Would you like to play against the bot? (y/n)")
    valid_answer = False
    while not valid_answer:
        answer = input()
        if answer == "y":
            play_game = True
            valid_answer = True
        elif answer == "n":
            print("Goodbye!")
            play_game = False
            valid_answer = True
        else:
            print("Error, please enter 'y' or 'n':")

    while play_game:
        board = Board()
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
            bot = Bot("O",bot2.V,bot2.num_wins,0,False) #Load key bot variables from previous trials
            player_symbol = "X"
        else:
            bot = Bot("X",bot1.V,bot1.num_wins,0,False) #Load key bot variables from previous trials
            player_symbol = "O"

        ##Run the game##
        MAX_NUM_TURNS = 9
        turn = 1
        victory = False
        board.print_board()
        while turn <= MAX_NUM_TURNS and not victory:
            cur_player = (turn-1)%2 + 1
            if cur_player == player:
                print("Please make a move. Available moves:")
                print(board.available_moves)
                move = input()
                while move.isdigit() == False:
                    print("Error, please try again:")
                    move = input()
                move = int(move)
                while move not in board.available_moves:
                    print("Error: move unavailable. Available moves:")
                    print(board.available_moves)
                    move = input()
                    while move.isdigit() == False:
                        print("Error, please try again:")
                        move = input()
                    move = int(move)
                board.update(move,player_symbol)
            
            else:
                n_states = board.get_next_possible_states(bot.symbol)
                for mov, state in n_states.items():
                    if state in bot.V:
                        print("State " + state + " has value: " + str(bot.V[state]))
                    else:
                        print("State not analysed yet.")

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

def save_results(bot1,bot2,MAX_NUM,case):    
    path = os.getcwd() + os.sep
    res_dir = "tictactoeResults" + os.sep
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



    '''
    filename = "results_" + str(MAX_NUM) + "_" + case + ".txt"
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
    '''
    for state, value in bot1.V.items():
        f.write("-"*len(state_msg) + "\n")
        f.write(state[0:3] + " "*4 + "V(s) for X: " + str(round(value,3)) + "\n")
        f.write(state[3:6] + " "*4 + "V(s) for O: " + str(round(bot2.V[state],3)) +"\n")
        f.write(state[6:9] + "\n")

        

if __name__ == "__main__":
    main()

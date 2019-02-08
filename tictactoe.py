import numpy as np
import random
'''
Tic-tac-toe game.
Author: Max Croci
Date: 06.02.2019
'''

class Board:
    __xlocs = []
    __olocs = []
    __positions = {}
    __avail_positions = []
    visited_states = []
    V = {} #Value of states

    def __init__(self):
        self.__initialise()

    def __initialise(self): 
        for i in range(9):
            self.__positions[i] = "_"
            self.__avail_positions.append(i+1)
        self.visited_states.append("_________")
        self.print_board()

    def print_board(self):
        #print(self.__positions)
        row1 = ""
        row2 = ""
        row3 = ""
        for i in range(3):
            row1 += self.__positions[i]
            row2 += self.__positions[3+i]
            row3 += self.__positions[6+i]
        print(row1)
        print(row2)
        print(row3)

    def __update_positions(self):
        for [xi,xj] in self.__xlocs:
            self.__positions[3*xi + xj] = "X"
        for [oi,oj] in self.__olocs:
            self.__positions[3*oi + oj] = "O"

    def update_visited_states(self):
        row1 = ""
        row2 = ""
        row3 = ""
        for i in range(3):
            row1 += self.__positions[i]
            row2 += self.__positions[3+i]
            row3 += self.__positions[6+i]
        state = row1 + row2 + row3
        self.visited_states.append(state)

    def add_move(self, player, move):
        if move+1 not in self.__avail_positions:
            print("***Error: this move is invalid!")
            return False

        i = int(np.floor(move/3))
        j = move%3
        if player == 1:
            self.__xlocs.append([i,j])
        else:
            self.__olocs.append([i,j])
        
        self.__avail_positions.remove(move+1)
        self.__update_positions()
        self.update_visited_states()
        #print(self.visited_states)
        return True

    def print_avail_positions(self):
        print("Available positions: " + str([pos for pos in self.__avail_positions]))
    
    def check_victory(self, player):
        for i in range(3):
            if self.__positions[3*i] != "_" and self.__positions[3*i] ==  self.__positions[3*i+1]\
                    and self.__positions[3*i] ==  self.__positions[3*i+2]:
                
                print("1Player %i wins!" % player)
                self.V[self.visited_states[-1]] = 100
                return True 
            if self.__positions[i] != "_" and self.__positions[i] ==  self.__positions[i+3]\
                    and self.__positions[i] ==  self.__positions[i+6]:
            
                print("2Player %i wins!" % player)
                self.V[self.visited_states[-1]] = 100
                return True 

        if self.__positions[0] != "_" and self.__positions[0] ==  self.__positions[4]\
                and self.__positions[0] ==  self.__positions[8]:
            
            print("3Player %i wins!" % player)
            self.V[self.visited_states[-1]] = 100
            return True 
        
        if self.__positions[2] != "_" and self.__positions[2] ==  self.__positions[4]\
                and self.__positions[2] ==  self.__positions[6]:
            
            print("4Player %i wins!" % player)
            self.V[self.visited_states[-1]] = 100
            return True 

        return False

    def get_next_avail_states(self, player):
        if player == 1:
            symbol = "X"
        else:
            symbol = "O"

        cur_state = self.visited_states[-1]
        blank_pos = [pos for pos, char in enumerate(cur_state) if char == "_"]
        #print(blank_pos)
        next_avail_states = {} #Dict keyed by moves, values are states
        for pos in blank_pos:
            if pos == 0:
                new_state = symbol + cur_state[1:9]
                next_avail_states[pos+1] = new_state
            elif pos == 8:
                new_state = cur_state[0:8] + symbol
                next_avail_states[pos+1] = new_state
            else:
                new_state = cur_state[0:pos] + symbol + cur_state[pos+1:9]
                next_avail_states[pos+1] = new_state

        return next_avail_states

def main():
    print("Hello, welcome to tic-tac-toe!")
    board = Board()
    
    next_states = []
    turn_no = 1
    player = 1 
    next_states = board.get_next_avail_states(player)
    victory = False
    while turn_no < 10 and not victory: 
        print("#"*15)
        validMove = False
        while not validMove:
            print("Player " + str(player) + "'s go. Please enter a valid move:")
            board.print_avail_positions()
            
            '''
            move = input()
            if move.isdigit():
                move = int(move)
                validMove = board.add_move(player,move-1)
                board.print_board()
            else:
                print("***Error: incorrect entry. Entry must be an integer 1-9.")
            '''
            print("Ready?")
            m = input()

            move_list = []
            state_list = []
            max_state_V = -1000
            for poss_move, poss_state in next_states.items():
                if poss_state not in board.V.keys():
                    board.V[poss_state] = 0
                if board.V[poss_state] > max_state_V:
                    max_state_V = board.V[poss_state]
            
            for state, Vstate in board.V.items():
                if Vstate == max_state_V:
                    state_list.append(state)
            
            for move, state in next_states.items():
                if state in state_list:
                    move_list.append(move)

            move = random.choice(move_list)
            print(move)
            validMove = board.add_move(player,move-1)
            board.print_board()

        victory = board.check_victory(player)
        if turn_no%2 == 1:
            player = 2
        else:
            player = 1
        turn_no = turn_no + 1
        #print(board.V)
        next_states = board.get_next_avail_states(player)

    #If end is a draw, update V[final_state] to zero
    if not victory:
        final_state = board.visited_states[-1]
        board.V[final_state] = 0

    #Update V: Use temporal-difference learning to train the bot
    for state in board.visited_states:
        if state not in board.V:
            board.V[state] = 0
    n_states_visited = len(board.visited_states)
    #print(n_states_visited)
    for i in range(n_states_visited-1):
        state = board.visited_states[n_states_visited - i - 2]
        next_state = board.visited_states[n_states_visited - i - 1]
        board.V[state] = board.V[state] + 0.1*(board.V[next_state] - board.V[state])
    print("The estimated values of the states are:")
    print(board.V)

if __name__ == "__main__":
    main()

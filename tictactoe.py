import numpy as np
import random
'''
Tic-tac-toe game.
Author: Max Croci
Date: 06.02.2019
'''

xlocs = [] #List of indices of "X" symbols
olocs = [] #List of indices of "O" symbols
visited_states = [] #List of visited states
positions = {} #Dict of placing of symbols, keyed by positions 1-9
avail_positions = [] #List of possible moves 1-9

class Board:

    V = {} #Value of states

    def __init__(self,V):
        self.V = V
        self.__initialise()

    def __initialise(self):
        for i in range(9):
            positions[i] = "_"
        visited_states.append("_________")
        #self.print_board()

    def print_board(self):
        #print(positions)
        row1 = ""
        row2 = ""
        row3 = ""
        for i in range(3):
            row1 += positions[i]
            row2 += positions[3+i]
            row3 += positions[6+i]
        print(row1)
        print(row2)
        print(row3)

    def __update_positions(self):
        for [xi,xj] in xlocs:
            positions[3*xi + xj] = "X"
        for [oi,oj] in olocs:
            positions[3*oi + oj] = "O"

    def update_visited_states(self):
        row1 = ""
        row2 = ""
        row3 = ""
        for i in range(3):
            row1 += positions[i]
            row2 += positions[3+i]
            row3 += positions[6+i]
        state = row1 + row2 + row3
        visited_states.append(state)

    def add_move(self, player, move):
        if move not in positions:
            print("***Error: this move is invalid!")
            return False

        i = int(np.floor(move/3))
        j = move%3
        if player == 1:
            xlocs.append([i,j])
        else:
            olocs.append([i,j])
        
        avail_positions.remove(move+1)
        self.__update_positions()
        self.update_visited_states()
        #print(visited_states)
        return True

    def print_avail_positions(self):
        print("Available positions: " + str([pos for pos in avail_positions]))
    
    def check_victory(self, player):
        for i in range(3):
            if positions[3*i] != "_" and positions[3*i] ==  positions[3*i+1]\
                    and positions[3*i] ==  positions[3*i+2]:
                
                #print("Player %i wins!" % player)
                self.V[visited_states[-1]] = 100
                return True 
            if positions[i] != "_" and positions[i] ==  positions[i+3]\
                    and positions[i] ==  positions[i+6]:
            
                #print("Player %i wins!" % player)
                self.V[visited_states[-1]] = 100
                return True 

        if positions[0] != "_" and positions[0] ==  positions[4]\
                and positions[0] ==  positions[8]:
            
            #print("Player %i wins!" % player)
            self.V[visited_states[-1]] = 100
            return True 
        
        if positions[2] != "_" and positions[2] ==  positions[4]\
                and positions[2] ==  positions[6]:
            
            #print("Player %i wins!" % player)
            self.V[visited_states[-1]] = 100
            return True 

        return False

    def get_next_avail_states(self, player):
        if player == 1:
            symbol = "X"
        else:
            symbol = "O"

        cur_state = visited_states[-1]
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
    learning_rate = 0.05
    num_trials_list = [10**(i+1)  for i in range(4)]
    Xwins_list = []
    Owins_list = []

    for num_trials in num_trials_list:
        Vx = {}
        Vo = {}
        Xwins = 0
        Owins = 0
        for n in range(num_trials):
            if (n+1)%10 == 0:
                print("Trial : " + str(n+1) + "/" + str(num_trials))
            global xlocs 
            global olocs
            global visited_states
            global positions
            global avail_positions
            xlocs = [] #List of indices of "X" symbols
            olocs = [] #List of indices of "O" symbols
            visited_states = [] #List of visited states
            positions = {} #Dict of placing of symbols, keyed by positions 1-9
            avail_positions = [i + 1 for i in range(9)] #List of possible moves 1-9
            if n == 0:
                boardX = Board(Vx)
                boardO = Board(Vo)
                
            else:
                boardX = Board(boardX.V)
                boardO = Board(boardO.V)
            turn_no = 1
            player = 1 
            next_states = boardX.get_next_avail_states(player)
            victory = False

            while turn_no < 10 and not victory: 
                #print("#"*15)
                validMove = False

                while not validMove:
                    if player == 1:
                        board = boardX
                    else:
                        board = boardO

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
                    #if player == 2:
                    #    move = random.choice(avail_positions)
                    #print(move)
                    validMove = board.add_move(player,move-1)
                    #board.print_board()

                    victory = board.check_victory(player)
                    if (victory):
                        if player == 1:
                            boardX.V[visited_states[-1]] = 100
                            boardO.V[visited_states[-1]] = -100
                            Xwins = Xwins + 1
                        else:
                            boardX.V[visited_states[-1]] = -100
                            boardO.V[visited_states[-1]] = 100
                            Owins = Owins + 1

                    if player == 1:
                        next_states = boardX.get_next_avail_states(2)
                    else:
                        next_states = boardO.get_next_avail_states(1)
                    
                    if turn_no%2 == 1:
                        player = 2
                    else:
                        player = 1
                    turn_no = turn_no + 1


            ######END OF GAME########

            #If end is a draw, update V[final_state] to zero
            if not victory:
                final_state = visited_states[-1]
                boardX.V[final_state] = 0
                boardO.V[final_state] = 0

            #Update V: Use temporal-difference learning to train the bot
            for state in visited_states:
                if state not in boardX.V:
                    boardX.V[state] = 0
                if state not in boardO.V:
                    boardO.V[state] = 0
            
            n_states_visited = len(visited_states)
            for i in range(n_states_visited-1):
                state = visited_states[n_states_visited - i - 2]
                next_state = visited_states[n_states_visited - i - 1]
                boardX.V[state] = boardX.V[state] + learning_rate*(boardX.V[next_state] - boardX.V[state])
                boardO.V[state] = boardO.V[state] + learning_rate*(boardO.V[next_state] - boardO.V[state])
        print("Xwins: %i" % Xwins)
        Xwins_list.append(Xwins)
        print("Owins: %i" % Owins)
        Owins_list.append(Owins)

    ####PLAY THE BOT#####
    while True:
        xlocs = [] #List of indices of "X" symbols
        olocs = [] #List of indices of "O" symbols
        visited_states = [] #List of visited states
        positions = {} #Dict of placing of symbols, keyed by positions 1-9
        avail_positions = [i + 1 for i in range(9)] #List of possible moves 1-9
        
        print("Play as player '1' or '2'?:")
        chosen_player = int(input())
        
        boards = {}
        Vp = {}
        boardPlayer = Board(Vp)
        if chosen_player == 1: #Load appropriate bot (X or O)
            boardBot = Board(boardO.V)
            boards[1] = boardPlayer
            boards[2] = boardBot
        else:
            boardBot = Board(boardX.V)
            boards[1] = boardBot
            boards[2] = boardPlayer

        
        turn_no = 1
        player = 1
        next_states = boardBot.get_next_avail_states(player)
        victory = False

        while turn_no < 10 and not victory: 
            print("#"*15)
            validMove = False

            while not validMove:
                board = boards[player]

                print("Player " + str(player) + "'s go. Please enter a valid move:")
                board.print_avail_positions()
                
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
                if player == chosen_player:
                    move = int(input())
                    
                print(move)
                validMove = board.add_move(player,move-1)
                board.print_board()

                victory = board.check_victory(player)

                if player == 1:
                    next_states = board.get_next_avail_states(2)
                else:
                    next_states = board.get_next_avail_states(1)
                
                if turn_no%2 == 1:
                    player = 2
                else:
                    player = 1
                turn_no = turn_no + 1



if __name__ == "__main__":
    main()

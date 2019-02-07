import numpy as np
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

    def __init__(self):
        self.__initialise()

    def __initialise(self): 
        for i in range(9):
            self.__positions[i] = "_"
            self.__avail_positions.append(i+1)
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


    def add_move(self, player, move):
        i = int(np.floor(move/3))
        j = move%3
        if player == 1:
            self.__xlocs.append([i,j])
        else:
            self.__olocs.append([i,j])

        self.__avail_positions.remove(move+1)
        self.__update_positions()

    def print_avail_positions(self):
        print("Available positions:")
        print([pos for pos in self.__avail_positions])

def main():
    print("Hello, welcome to tic-tac-toe!")
    board = Board()
    #board.initialise()
    
    turn_no = 1
    player = 1
    
    while turn_no < 10:
        board.print_avail_positions()
        print("Player " + str(player) + "'s go. Please enter a number 1-9:")
        move = int(input())
        board.add_move(player,move-1)
        board.print_board()
        if turn_no%2 == 1:
            player = 2
        else:
            player = 1
        turn_no = turn_no + 1

if __name__ == "__main__":
    main()

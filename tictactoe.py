import numpy as np
'''
Tic-tac-toe game.
Author: Max Croci
Date: 06.02.2019
'''

class Board:
    busySquares = 0
    x_locs = []
    o_locs = []
    positions = {}

    def initialise(self): 
        for i in range(9):
            self.positions[i] = "_"
        self.print_board()

    def description(self):
        desc_str = "This board has %i busy squares" % (self.busySquares)
        return desc_str

    def print_board(self):
        print(self.positions)
        row1 = ""
        row2 = ""
        row3 = ""
        for i in range(3):
            row1 += self.positions[i]
            row2 += self.positions[3+i]
            row3 += self.positions[6+i]
        print(row1)
        print(row2)
        print(row3)

    def update_positions(self):
        for [xi,xj] in self.x_locs:
            self.positions[3*xi + xj] = "X"
        for [oi,oj] in self.o_locs:
            self.positions[3*oi + oj] = "O"

    def add_move(self, player, move):
        i = int(np.floor(move/3))
        j = move%3
        if player == 1:
            self.x_locs.append([i,j])
        else:
            self.o_locs.append([i,j])

        self.update_positions()

def main():
    print("Hello, welcome to tic-tac-toe!")
    board = Board()
    board.initialise()
    
    turn_no = 1
    player = 1
    
    while turn_no < 10:
        print("Player " + str(player) + "'s go. Please enter a number 0-8:")
        move = int(input())
        board.add_move(player,move)
        board.print_board()
        if turn_no%2 == 1:
            player = 2
        else:
            player = 1
        turn_no = turn_no + 1

if __name__ == "__main__":
    main()

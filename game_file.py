import math
import sys
import random

class board:
    def __init__(self, size, bombs):
        self.bombs = bombs
        self.size = size
        self.board = []

    def build_board_spaces(self):
        i = 0
        j = 0

        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
        return

    def place_bombs(self):
        i = 0
        while i < self.bombs:
            row = random.randint(0, self.size-1)
            col = random.randint(0, self.size-1)
            if self.board[row][col] != 9:
                self.board[row][col] = 9
                i += 1
            else:
                pass
        return

    def bomb_check(self, row, col):
        if self.board[row][col] == 9:
            return True
        else:
            return False

    def assign_index_value(self, row, col):

        counter = 0

        if (row - 1 >= 0) and (self.board[row-1][col] == 9):

            counter += 1

        if (row + 1 < self.size-1) and (self.board[row+1][col] == 9):

            counter += 1

        if (col - 1 >= 0) and (self.board[row][col-1] == 9):

            counter += 1

        if (col + 1 < self.size-1) and (self.board[row][col+1] == 9):

            counter += 1

        if (row - 1 >= 0) and (col - 1 >= 0) and (self.board[row-1][col-1] == 9):

            counter += 1

        if (row - 1 >= 0) and (col + 1 < self.size-1) and (self.board[row-1][col+1] == 9):

            counter += 1

        if (row + 1 < self.size-1) and (col - 1 >= 0) and (self.board[row+1][col-1] == 9):

            counter += 1

        if (row + 1 < self.size-1) and (col + 1 < self.size-1) and (self.board[row+1][col+1] == 9):

            counter += 1

        return counter
        

    def assign_values(self):

        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.board[row][col] == 0: 
                    self.board[row][col] = self.assign_index_value(row, col)
                col += 1
            row += 1

    def print_board(self):
        for x in range(0,self.size):
            for y in range(0,self.size):
                print(self.board[x][y], end="")
                y += 1
            x += 1

            print('\n')
        return

def main():
    size = int(input("Hello welcome to minesweeper. How big would you like the board?\n"))
    bombs = int(input("How many bombs would you like?\n"))
    Board = board(size, bombs)
    Board.build_board_spaces()
    Board.place_bombs()
    Board.assign_values()
    Board.print_board()
    return

if __name__ == "__main__":
    main()

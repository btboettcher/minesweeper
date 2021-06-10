import math
import sys
import random

class board:
    def __init__(self, length, width, bombs):
        self.bombs = bombs
        self.length = length
        self.width = width
        self.board = []
        self.game_over = 0
        self.game_won = 0

    def build_board_spaces(self):
        i = 0
        j = 0

        self.board = [[0 for i in range(self.width)] for j in range(self.length)]
        return

    def place_bombs(self):
        i = 0
        while i < self.bombs:
            row = random.randint(0, self.length-1)
            col = random.randint(0, self.width-1)
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

        if (row + 1 < self.length) and (self.board[row+1][col] == 9):
            counter += 1

        if (col - 1 >= 0) and (self.board[row][col-1] == 9):
            counter += 1

        if (col + 1 < self.width) and (self.board[row][col+1] == 9):
            counter += 1

        if (row - 1 >= 0) and (col - 1 >= 0) and (self.board[row-1][col-1] == 9):
            counter += 1

        if (row - 1 >= 0) and (col + 1 < self.width) and (self.board[row-1][col+1] == 9):
            counter += 1

        if (row + 1 < self.length) and (col - 1 >= 0) and (self.board[row+1][col-1] == 9):
            counter += 1

        if (row + 1 < self.length) and (col + 1 < self.width) and (self.board[row+1][col+1] == 9):
            counter += 1

        return counter
        

    def assign_values(self):

        for row in range(0, self.length):
            for col in range(0, self.width):
                if self.board[row][col] == 0: 
                    self.board[row][col] = self.assign_index_value(row, col)
                col += 1
            row += 1

    def print_board(self):
        for x in range(0,self.length):
            for y in range(0,self.width):
                print(self.board[x][y], end="")
                y += 1
            x += 1

            print('\n')
        return

    def set_up(self):
        self.build_board_spaces()
        self.place_bombs()
        self.assign_values()

class ViewBoard:

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.view_board = []

    def v_set_up(self):
        self.view_board = [[' # ' for i in range(self.width)] for j in range(self.length)]
    
    def print_board(self):
        for x in range(0,self.length):
            for y in range(0,self.width):
                print(self.view_board[x][y], end="")
                y += 1
            x += 1

            print('\n')
        return
    
    def flower(self, base_board, row, column):

        if row > -1 and column > -1 and row < self.length and column < self.width:

            if base_board.board[row][column] >= 1 and base_board.board[row][column] <= 8:
                self.view_board[row][column] = " " + str(base_board.board[row][column]) + " "
                return

            elif self.view_board[row][column] == ' # ' and base_board.board[row][column] == 0:
                self.view_board[row][column] = " " + str(base_board.board[row][column]) + " "
                self.flower(base_board, row-1, column-1)
                self.flower(base_board, row-1, column)
                self.flower(base_board, row-1, column+1)
                self.flower(base_board, row, column-1)
                self.flower(base_board, row, column+1)
                self.flower(base_board, row+1, column-1)
                self.flower(base_board, row+1, column)
                self.flower(base_board, row+1, column+1)
        else:
            return


    def reveal(self, base_board, row, column):
        
        if base_board.board[row][column] == 9:
            base_board.game_over = 1
            return

        else:
            self.flower(base_board, row, column)

    def flag(self, base_board, row, column):

        self.view_board[row][column] = ' ? '

    def unflag(self, base_board, row, column):

        self.view_board[row][column] = ' # '

    def is_game_won(self, base_board):

        bomb_counter = 0
        nonbombs_revealed = False
        
        #make sure all bombs have been flagged
        if base_board.game_over != 1 and base_board.game_won != 1:
            for i in range(0, self.length):
                for j in range(0, self.width):
                    if base_board.board[i][j] == 9 and self.view_board[i][j] == ' ? ':
                        bomb_counter += 1
            
        #make sure all non-bomb squares have been revealed
        if base_board.game_over != 1 and base_board.game_won != 1:
            for k in range(0, self.length):
                for l in range(0, self.width):
                    if base_board.board[k][l] != 9 and self.view_board[k][l] == ' # ':
                        nonbombs_revealed = False
                    else:
                        nonbombs_revealed = True
        
        if bomb_counter == base_board.bombs and nonbombs_revealed:
            base_board.game_won = 1
        
        return
        

def set_up():
    #get parameters for board
    while True:
        try:
            length = int(input("Hello welcome to minesweeper. What would you like the length of the board to be? (Max 99 min 1\n"))
            width = int(input("Width?\n"))
            bombs = int(input("How many bombs would you like?\n"))
        except:
            print("Not valid input. Max length and width is 99. Max amount of bombs is 1000")
            continue
        else:
            break

    return [length, width, bombs]


def choice_menu():

    choice = int(input(
    """
    Select your choice for this turn:
    1 - Reveal a tile
    2 - Flag a tile
    3 - Unflag a tile\n"""))

    row = int(input("Which row?"))
    column = int(input("which column?"))

    return [choice, row, column]

def game_won(ViewBoard):
    print("Congratulations! You've won!")
    ViewBoard.print_board()

def game_over(base_board):
    print("You hit a bomb! Sorry you lose.")
    base_board.print_board()

def play_game(base_board, ViewBoard):

    while (base_board.game_over != 1 and base_board.game_won != 1):
        base_board.print_board()
        ViewBoard.print_board()
        turn_parameters = choice_menu()

        if turn_parameters[0] == 1:
            ViewBoard.reveal(base_board, turn_parameters[1], turn_parameters[2])
        if turn_parameters[0] == 2:
            ViewBoard.flag(base_board, turn_parameters[1], turn_parameters[2])
        if turn_parameters[0] == 3:
            ViewBoard.unflag(base_board, turn_parameters[1], turn_parameters[2])

        ViewBoard.is_game_won(base_board)
        
    if base_board.game_over == 1:
        ViewBoard.game_over(base_board)
    elif base_board.game_won == 1:
        game_won(ViewBoard)

def main():

    board_parameters = set_up()
    #Set up the base board that holds all the integer values of each square
    BaseBoard = board(board_parameters[0], board_parameters[1], board_parameters[2])
    BaseBoard.set_up()

    #set up the board viewed by the player
    TopBoard = ViewBoard(board_parameters[0], board_parameters[1])
    TopBoard.v_set_up()

    play_game(BaseBoard, TopBoard)

    return

if __name__ == "__main__":
    main()

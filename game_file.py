import math
import sys
import random

# Per Wikipedia
# Minesweeper is a single-player puzzle video game. The objective is to clear a rectangular board containing hidden bombs without detonating any of them, with help from clues
# about the number of neighboring mines in each field. If a player reveals a square containing a mine, they lose the game. If no mine is revealed, a digit is instead displayed
# in the square, indicating how many adjacent squares contain mines. If no mines are adjacent, the square becomes blank, and all adjacent squares will be recursively revealed.

BOMB = 9

# ---------------Algo Solver Class --------------------
# row_choice: row of move
# Column_choice: column of move
# frontier: list of tiles that border unexplored area of the border
# safe: list of tiles that are safe to reveal 

class algo_solver:
    def __init__(self):
        self.row_choice = 0
        self.column_choice = 0
        self.frontier = []
        self.safe = []

    def marked_neighbors(self, base_board, view_board):

        #marked tiles are those that equal = ?. Used in the AFN function to determine if a tiles neighbors are safe

        marked = 0
        #top
        if (self.row_choice - 1 >= 0) and view_board.view_board[self.row_choice-1][self.column_choice] == ' ? ':
            marked += 1
        #bottom
        if (self.row_choice + 1 < view_board.length) and view_board.view_board[self.row_choice+1][self.column_choice] == ' ? ':
            marked += 1
        #left
        if (self.column_choice - 1 >= 0) and view_board.view_board[self.row_choice][self.column_choice-1] == ' ? ':
            marked += 1
        #right
        if (self.column_choice + 1 < view_board.width) and view_board.view_board[self.row_choice][self.column_choice+1] == ' ? ':
            marked += 1
        #top left
        if (self.row_choice - 1 >= 0) and (self.column_choice - 1 >= 0) and view_board.view_board[self.row_choice-1][self.column_choice-1] == ' ? ':
            marked += 1
        #top right
        if (self.row_choice - 1 >= 0) and (self.column_choice + 1 < view_board.width) and view_board.view_board[self.row_choice-1][self.column_choice+1] == ' ? ':
            marked += 1
        #bottom left
        if (self.row_choice + 1 < view_board.length) and (self.column_choice - 1 >= 0) and view_board.view_board[self.row_choice+1][self.column_choice-1] == ' ? ':
            marked += 1
        #bottom right
        if (self.row_choice + 1 < view_board.length) and (self.column_choice + 1 < view_board.width) and view_board.view_board[self.row_choice+1][self.column_choice+1] == ' ? ':
            marked += 1

        return marked
    
    def unmarked_calculator_AFN(self, base_board, view_board):

        #specifices that the definition of an unmarked tile for AFN function is a tile that = #. Makes list that is appended to the safe list

        unmarked = 0
        unmarked_list = []

        if (self.row_choice - 1 >= 0) and (view_board.view_board[self.row_choice-1][self.column_choice] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice-1, self.column_choice])

        if (self.row_choice + 1 < view_board.length) and (view_board.view_board[self.row_choice+1][self.column_choice] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice+1, self.column_choice])

        if (self.column_choice - 1 >= 0) and (view_board.view_board[self.row_choice][self.column_choice-1] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice, self.column_choice-1])

        if (self.column_choice + 1 < view_board.width) and (view_board.view_board[self.row_choice][self.column_choice+1] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice, self.column_choice+1])

        if (self.row_choice - 1 >= 0) and (self.column_choice - 1 >= 0) and (view_board.view_board[self.row_choice-1][self.column_choice-1] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice-1, self.column_choice-1])

        if (self.row_choice - 1 >= 0) and (self.column_choice + 1 < view_board.width) and (view_board.view_board[self.row_choice-1][self.column_choice+1] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice-1, self.column_choice+1])

        if (self.row_choice + 1 < view_board.length) and (self.column_choice - 1 >= 0) and (view_board.view_board[self.row_choice+1][self.column_choice-1] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice+1, self.column_choice-1])

        if (self.row_choice + 1 < view_board.length) and (self.column_choice + 1 < view_board.width) and (view_board.view_board[self.row_choice+1][self.column_choice+1] == ' # '):
            unmarked += 1
            unmarked_list.append([self.row_choice+1, self.column_choice+1])

        return [unmarked, unmarked_list]

    def unmarked_calculator(self, base_board, view_board):

        #If the tile neighbors equals # or ? then it is an unmarked tile (not revealed). Provides list of tiles that are subsequently flagged as mines in the AMN function

        unmarked = 0
        unmarked_list = []

        if (self.row_choice - 1 >= 0) and (view_board.view_board[self.row_choice-1][self.column_choice] == ' # ' or view_board.view_board[self.row_choice-1][self.column_choice] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice-1, self.column_choice])

        if (self.row_choice + 1 < view_board.length) and (view_board.view_board[self.row_choice+1][self.column_choice] == ' # ' or view_board.view_board[self.row_choice+1][self.column_choice] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice+1, self.column_choice])

        if (self.column_choice - 1 >= 0) and (view_board.view_board[self.row_choice][self.column_choice-1] == ' # ' or view_board.view_board[self.row_choice][self.column_choice-1] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice, self.column_choice-1])

        if (self.column_choice + 1 < view_board.width) and (view_board.view_board[self.row_choice][self.column_choice+1] == ' # ' or view_board.view_board[self.row_choice][self.column_choice+1] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice, self.column_choice+1])

        if (self.row_choice - 1 >= 0) and (self.column_choice - 1 >= 0) and (view_board.view_board[self.row_choice-1][self.column_choice-1] == ' # ' or view_board.view_board[self.row_choice-1][self.column_choice-1] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice-1, self.column_choice-1])

        if (self.row_choice - 1 >= 0) and (self.column_choice + 1 < view_board.width) and (view_board.view_board[self.row_choice-1][self.column_choice+1] == ' # ' or view_board.view_board[self.row_choice-1][self.column_choice+1] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice-1, self.column_choice+1])

        if (self.row_choice + 1 < view_board.length) and (self.column_choice - 1 >= 0) and (view_board.view_board[self.row_choice+1][self.column_choice-1] == ' # ' or view_board.view_board[self.row_choice+1][self.column_choice-1] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice+1, self.column_choice-1])

        if (self.row_choice + 1 < view_board.length) and (self.column_choice + 1 < view_board.width) and (view_board.view_board[self.row_choice+1][self.column_choice+1] == ' # ' or view_board.view_board[self.row_choice+1][self.column_choice+1] == ' ? '):
            unmarked += 1
            unmarked_list.append([self.row_choice+1, self.column_choice+1])

        return [unmarked, unmarked_list]

    #label of the tile equals the number of marked neighbors (marked tiles = ?) (all free)
    #all tiles that are not marked are labeled as safe in the algorithm
    def isAFN(self, base_board, view_board):
        tile_value = base_board.board[self.row_choice][self.column_choice] # 0
        marked_neighbors = self.marked_neighbors(base_board, view_board) # = ' ? '

        if tile_value == marked_neighbors:
            return True
        else:
            return False

    #label of the tile equals the number of unmarked neighbors (all mines)
    #All unmarked tiles are mines and are flagged as such in the algorithm
    def isAMN(self, base_board, view_board):
        tile_value = base_board.board[self.row_choice][self.column_choice]
        unmarked_neighbors = self.unmarked_calculator(base_board, view_board)[0]

        if tile_value == unmarked_neighbors:
            return True
        else:
            return False

    
    def algo_double_set(self, base_board, view_board):

        #reveals the top left corner. The default first move
        view_board.reveal(base_board, view_board, self.row_choice, self.column_choice)

        #appends to begin algorithm
        self.safe.append([self.row_choice, self.column_choice])

        while (base_board.game_over != 1 and base_board.game_won != 1):
            base_board.print_board()
            view_board.print_board()

            #Randomly selects row and column if no tiles are guaranteed safe
            if len(self.safe) == 0:
                self.row_choice = random.randint(0, base_board.length-1)
                self.column_choice = random.randint(0, base_board.width-1)
                self.safe.append([self.row_choice, self.column_choice])

            #while the sade list is not empty
            
            while (len(self.safe) != 0):
                last_element = self.safe.pop(0)         #pops element from safe to look at
                self.row_choice = last_element[0]       #sets it as the move
                self.column_choice = last_element[1]
                print("Row: " + str(self.row_choice))
                print("Column: " + str(self.column_choice))
                if view_board.view_board[self.row_choice][self.column_choice] == ' ? ':
                    break
                view_board.reveal(base_board, view_board, self.row_choice, self.column_choice)
                base_board.print_board()
                view_board.print_board()
                if base_board.game_over == 1:           #checks to ensure bomb was not revealed
                    view_board.view_board[self.row_choice][self.column_choice] = ' X '
                    return
                if self.isAFN(base_board, view_board): #Surrounding unmarked tiles are free add them to the safe list
                    for tile in self.unmarked_calculator_AFN(base_board, view_board)[1]:
                        if tile in self.safe:
                            continue
                        else:
                            self.safe.append(tile)
                else:
                    if last_element in self.frontier:
                        continue
                    else:
                        self.frontier.append(last_element)

            #Safe list has no tiles to pop, begin looking at the frontier list
            
            for q in self.frontier:
                self.row_choice = q[0]
                self.column_choice = q[1]
                if self.isAMN(base_board, view_board): #all unmarked tiles are bombs, flag them as such
                    for y in self.unmarked_calculator(base_board, view_board)[1]:
                        view_board.flag(base_board, y[0], y[1])
                        view_board.print_board()
                    self.frontier.remove(q)
            
            #check if AFN again on the frontier tiles to see if the new information from the flagged loop enabled AFN for some tiles
            for tile in self.frontier:
                self.row_choice = tile[0]
                self.column_choice = tile[1]
                if self.isAFN(base_board, view_board):
                    self.safe.append(tile)
                    self.frontier.remove(tile)

            view_board.is_game_won(base_board)


# ---------------Board Class --------------------
# bombs: number of bombs on the board
# length: length of the board
# width: width of the board
# board: empty list that will be filled with tiles
# game_over: flag for when game is over (hit a bomb)
# game_won: flag for when the game is won (all non-bomb tiles revealed and all bombs marked)


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
            if self.board[row][col] != BOMB:
                self.board[row][col] = BOMB
                i += 1
            else:
                pass
        return

    def bomb_check(self, row, col):
        if self.board[row][col] == BOMB:
            return True
        else:
            return False

    #counts how many bombs are around a specific square and returns counter
    def assign_index_value(self, row, col):

        counter = 0

        if (row - 1 >= 0) and (self.board[row-1][col] == BOMB):
            counter += 1

        if (row + 1 < self.length) and (self.board[row+1][col] == BOMB):
            counter += 1

        if (col - 1 >= 0) and (self.board[row][col-1] == BOMB):
            counter += 1

        if (col + 1 < self.width) and (self.board[row][col+1] == BOMB):
            counter += 1

        if (row - 1 >= 0) and (col - 1 >= 0) and (self.board[row-1][col-1] == BOMB):
            counter += 1

        if (row - 1 >= 0) and (col + 1 < self.width) and (self.board[row-1][col+1] == BOMB):
            counter += 1

        if (row + 1 < self.length) and (col - 1 >= 0) and (self.board[row+1][col-1] == BOMB):
            counter += 1

        if (row + 1 < self.length) and (col + 1 < self.width) and (self.board[row+1][col+1] == BOMB):
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


# ---------------display_board Class --------------------
# length: length of the board
# width: width of the board
# view_board: Board that holds the # values until revealed

class display_board:

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.view_board = []

    #initializes board with # characters
    def view_board_set_up(self):
        self.view_board = [[' # ' for i in range(self.width)] for j in range(self.length)]
    
    def print_board(self):
        for x in range(0,self.length):
            for y in range(0,self.width):
                print(self.view_board[x][y], end="")
                y += 1
            x += 1

            print('\n')
        return
    
    #recursion to reveal all tiles around the picked square if it equals 0. Will stop when tiles that are not 0 are discovered
    #ONLY USED WHEN HUMAN IS PLAYING THE GAME
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


    def reveal(self, base_board, view_board, row, column):

        if view_board.view_board[row][column] == ' ? ':
            return
        
        if base_board.board[row][column] == BOMB:
            base_board.game_over = 1
            return

        else:
            self.view_board[row][column] = " " + str(base_board.board[row][column]) + " "
            #self.flower(base_board, row, column) ONLY USED WHEN HUMAN IS PLAYING GAME

    def flag(self, base_board, row, column):

        self.view_board[row][column] = ' ? '

    def unflag(self, base_board, row, column):

        self.view_board[row][column] = ' # '

    def is_game_won(self, base_board):

        bomb_counter = 0
        nonbombs_revealed = 0
        
        #make sure all bombs have been flagged
        if base_board.game_over != 1 and base_board.game_won != 1:
            for i in range(0, self.length):
                for j in range(0, self.width):
                    if base_board.board[i][j] == BOMB and self.view_board[i][j] == ' ? ':
                        bomb_counter += 1
            
        #make sure all non-bomb squares have been revealed
        if base_board.game_over != 1 and base_board.game_won != 1:
            for k in range(0, self.length):
                for l in range(0, self.width):
                    if base_board.board[k][l] != BOMB and (self.view_board[k][l] == ' # ' or self.view_board[k][l] == ' ? '):
                        nonbombs_revealed += 1
                    else:
                        continue
        
        if bomb_counter == base_board.bombs and nonbombs_revealed == 0:
            base_board.game_won = 1
        
        return

#Used when a human is playing the game to validate input
def validate_pos_num(prompt, min, max):
    while True:
        try:
            answer = int(input(prompt))
        except:
            print("Not valid input. Min is " + str(min) + ", Max is " + str(max))
            continue

        if answer < min or answer > max:
            print("Not in range. Min is " + str(min) + ", Max is " + str(max))
            continue
        else:
            break
    return answer
        

def set_up():

    #get parameters for board
    #Beginner width - 9 length - 9 mines - 10
    #Intermediate width - 16 length - 16 mines - 40
    #Expert width - 30 legnth - 16 mines - 99

    #-------------------------------------------Only used when human is playing the game ---------------------------------------
    
    # length = validate_pos_num("Hello welcome to minesweeper. What would you like the length of the board to be?\n", 1, 99)
    # width = validate_pos_num("Width?\n", 1, 99)
    # bombs = validate_pos_num("How many bombs would you like?\n", 1, round((length * width)/2))

    #---------------------------------------------------------------------------------------------------------------------------

    #fixed to a beginner sized board for the algorithm to solve
    length = 9
    width = 9
    bombs = 10

    return [length, width, bombs]


#funtion is only used when a human is playing a game
def choice_menu(base_board, display_board, algo_solver):

    choice = validate_pos_num(
    """
    Select your choice for this turn:
    1 - Reveal a tile
    2 - Flag a tile
    3 - Unflag a tile\n""", 1, 3)

    row = validate_pos_num("Which row?", 0, base_board.length-1)
    column = validate_pos_num("which column?", 0, base_board.width-1)

    return [choice, row, column]

def game_won(display_board):
    print("Congratulations! You've won!")
    display_board.print_board()

def game_over(base_board, view_board):
    print("You hit a bomb! Sorry you lose.")
    base_board.print_board()
    view_board.print_board()


#Algorithm plays the game until it wins or loses.
def play_game(base_board, display_board, algo_solver):

    while (base_board.game_over != 1 and base_board.game_won != 1):
        

        algo_solver.algo_double_set(base_board, display_board)

        # ----------------------------Only used when human is playing the game ---------------------------------------

        # turn_parameters = choice_menu(base_board, display_board, algo_solver)

        # if turn_parameters[0] == 1:
        #     display_board.reveal(base_board, turn_parameters[1], turn_parameters[2])
        # if turn_parameters[0] == 2:
        #     display_board.flag(base_board, turn_parameters[1], turn_parameters[2])
        # if turn_parameters[0] == 3:
        #     display_board.unflag(base_board, turn_parameters[1], turn_parameters[2])

        # -------------------------------------------------------------------------------------------------------------

        display_board.is_game_won(base_board)
        
    if base_board.game_over == 1:
        game_over(base_board, display_board)
    elif base_board.game_won == 1:
        game_won(display_board)

def main():

    board_parameters = set_up()
    #Set up the base board that holds all the integer values of each square
    base_board = board(board_parameters[0], board_parameters[1], board_parameters[2])
    base_board.set_up()

    #set up the board viewed by the player. Will start with # in every position
    view_board = display_board(board_parameters[0], board_parameters[1])
    view_board.view_board_set_up()

    #initializes the algorithm setting its first move to be the top left corner
    discovery = algo_solver()

    play_game(base_board, view_board, discovery)

    return

if __name__ == "__main__":
    main()

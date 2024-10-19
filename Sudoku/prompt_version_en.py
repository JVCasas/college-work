import random

######## CLASSES ########

class Sudoku:  # Class that generates a Sudoku
    
    def __init__(self, difficulty):
        self.difficulty = difficulty  # Variable that receives a value from one to three to define the game difficulty, defaulting to easy
        self.complete_game = self.generate_complete_sudoku()  # Variable that receives a complete table (answer key)
        self.puzzle = self.generate_sudoku_puzzle(self.complete_game, self.difficulty)  # Variable that receives a puzzle based on the complete table

    def generate_complete_sudoku(self):  # Function that creates a complete Sudoku table (already solved)
        grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]  # Base matrix to be formatted
        reference_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Reference list of numbers to be inserted
        options = reference_options[:]

        def insert_random_number(matrix, reference, opts, row=0, column=0):  # Function that replaces the 0s in the matrix with random numbers to create a valid, complete Sudoku table
            
            if column >= 9:
                row += 1
                column = 0
                opts = reference[:]

            if row >= 9:
                return False
            else:
                if self.validate_options(row, column, opts, matrix):
                    valid_options = []
                    for n in opts:
                        if self.check_number(n, row, column, matrix):
                            valid_options.append(n)
                    while self.check_incompleteness(matrix):
                        if not valid_options:
                            return True
                        else:
                            number = random.choice(valid_options)
                            matrix[row][column] = number
                            opts.remove(number)
                            if insert_random_number(matrix, reference, opts, row, column + 1):
                                valid_options.remove(number)
                                opts.append(number)
                                opts.sort()
                                matrix[row][column] = 0
                    return False
                else:
                    return True

        insert_random_number(grid, reference_options, options)

        return grid
    
    def generate_sudoku_puzzle(self, matrix, difficulty=1):  # Function that takes a complete Sudoku table and removes random numbers to create a Sudoku puzzle according to the given difficulty
        resolution_copy = [row[:] for row in matrix]
        
        if difficulty == 1:
            removed_numbers = random.choice(range(31, 46))
        elif difficulty == 2:
            removed_numbers = random.choice(range(46, 61))
        else:
            removed_numbers = random.choice(range(61, 76))

        def find_solution(matrix, row=0, column=0, counter=0):  # Function that searches for the number of possible solutions for a puzzle
            if column >= 9:
                row += 1
                column = 0
            
            if row >= 9:
                counter += 1
                return counter
            else:
                if matrix[row][column] == 0:
                    for n in range(1, 10):
                        if self.check_number(n, row, column, matrix):
                            matrix[row][column] = n
                            counter += find_solution(matrix, row, column + 1)
                    matrix[row][column] = 0
                    return counter
                else:
                    counter += find_solution(matrix, row, column + 1)
                    return counter
        
        while removed_numbers > 0:
            row = random.choice(range(0, 8))
            column = random.choice(range(0, 8))
            rescue = resolution_copy[row][column]
            resolution_copy[row][column] = 0
            if find_solution(resolution_copy) != 1:
                resolution_copy[row][column] = rescue
            else:
                removed_numbers -= 1
        
        return resolution_copy

    @staticmethod
    def check_incompleteness(matrix):  # Function that checks if the table is completely filled
        for l in matrix:
            if 0 in l:
                return True
        return False

    @staticmethod
    def check_row(number, row, matrix):  # Function that checks if a number is not already in the row
        if number in matrix[row]:
            return False
        else:
            return True

    @staticmethod
    def check_column(number, column, matrix):  # Function that checks if a number is not already in the column
        col = []
        for lin in matrix:
            col.append(lin[column])
        if number in col:
            return False
        return True

    @staticmethod
    def check_sub_matrix(number, row, column, matrix):  # Function that checks if a number is not already in the 3x3 quadrant
        submatrix = []
        if row < 3:
            if column < 3:
                for n in range(0, 3):
                    submatrix.append(matrix[n][0:3])
            elif column < 6:
                for n in range(0, 3):
                    submatrix.append(matrix[n][3:6])
            else:
                for n in range(0, 3):
                    submatrix.append(matrix[n][6:9])
        elif row < 6:
            if column < 3:
                for n in range(3, 6):
                    submatrix.append(matrix[n][0:3])
            elif column < 6:
                for n in range(3, 6):
                    submatrix.append(matrix[n][3:6])
            else:
                for n in range(3, 6):
                    submatrix.append(matrix[n][6:9])
        else:
            if column < 3:
                for n in range(6, 9):
                    submatrix.append(matrix[n][0:3])
            elif column < 6:
                for n in range(6, 9):
                    submatrix.append(matrix[n][3:6])
            else:
                for n in range(6, 9):
                    submatrix.append(matrix[n][6:9])
        
        if number in (submatrix[0] + submatrix[1] + submatrix[2]):
            return False
        else:
            return True
    
    def check_number(self, number, row, column, matrix):  # Function that checks if the number can be inserted in the given position
        if self.check_row(number, row, matrix):
            if self.check_column(number, column, matrix):
                if self.check_sub_matrix(number, row, column, matrix):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def validate_options(self, row, column, options, matrix):  # Function that checks if there are valid number options to be inserted in the grid
        if options == []:
            return False
        
        for item in options:
            if self.check_number(item, row, column, matrix):
                return True
            
class Game:  # Class responsible for generating a game and managing its main functionalities
    def __init__(self):
        self.level = self.difficulty_menu()
        self.game = Sudoku(difficulty=self.level)
        self.answer_key = self.game.complete_game
        self.puzzle = self.game.puzzle
    
    @staticmethod
    def print_sudoku(matrix):  # Function that displays the formatted Sudoku table
        for l in range(0, 9):
            if l == 3 or l == 6:
                print('-' * 29)

            for n in range(0, 9):
                
                if n == 3 or n == 6:
                    print('|', end='')

                if matrix[l][n] == 0:
                    print(' . ', end='')
                else:
                    print(f' {matrix[l][n]} ', end='')
            print('')

    @staticmethod
    def difficulty_menu():  # Function that displays a difficulty selection menu
        print('Select a difficulty:\n[1] - Easy\n[2] - Intermediate\n[3] - Hard')
        while True:
            difficulty = input('Difficulty? -> ')
            if not difficulty.isnumeric():
                print('Please enter ONLY A SINGLE VALID NUMBER!')
            else:
                difficulty = int(difficulty)
                if difficulty in [1, 2, 3]:
                    return difficulty
                else:
                    print('Please enter ONLY A SINGLE VALID NUMBER!')

    @staticmethod
    def numeric_selection(input_message, start, end):  # Function that displays a submenu that returns a number entered by the user within a specified range
        while True:
            value = input(input_message)
            if not value.isnumeric():
                print('Please enter ONLY A SINGLE VALID NUMBER!')
            else:
                value = int(value)
                if value in range(start, end):
                    return value

    def game_menu(self):  # Function that displays a game menu and persists until the game is finished
        answer = self.answer_key
        puzzle = self.puzzle
        puzzle_copy = [row[:] for row in puzzle]

        while not puzzle == answer:
            self.print_sudoku(puzzle)
            row = self.numeric_selection('Enter a row from 1 to 9: ', 1, 10) - 1
            column = self.numeric_selection('Enter a column from 1 to 9: ', 1, 10) - 1
            if puzzle_copy[row][column] == 0:
                number = self.numeric_selection('Enter a number from 1 to 9 (Enter 0 to erase): ', 0, 10)
                if self.game.check_number(number, row, column, puzzle):
                    puzzle[row][column] = number
                else:
                    print('The number cannot be inserted in this cell.')
            else:
                print('You cannot select predefined cells!')
        print('Table Completed!')
        self.print_sudoku(answer)

######## FUNCTIONS ########

def continue_menu():  # Menu function that asks at the end of each game if a new game should be generated
    while True:
        entry = input('Do you want to continue? [Y/N] \n')
        if entry not in ['Y', 'y', 'N', 'n']:
            print('Invalid Input!')
        else:
            if entry in ['y', 'Y']:
                return True
            else:
                return False

######## PROGRAM ########

print(""" ________   __     __  _______    _________   __   ___   __     __ \n|  ______| |  |   | | |   __  \\  |   ____  | |  | /  /  |  |   | | \n|  |_____  |  |   | | |  |   \\ \\ |  |    | | |  |/  /   |  |   | | \n|______  | |  |   | | |  |   / / |  |    | | |   _  \\   |  |   | | \n_______| | |  |___| | |  |__/ /  |  |____| | |  | \\  \\  |  |___| | \n|________| |________| |______/   |_________| |__|  \\__\\ |________| \n""")
input('Press Enter to start a new game.')

continuation = True

while continuation:
    game = Game()
    game.game_menu()
    continuation = continue_menu()
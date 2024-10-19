import random
import unicodedata
import time
import os

def check_file(target):  # Function to check the existence and consistency of the database file
    """
    Checks the existence of the database file, and if it exists, searches for inconsistencies.

    Args:
        target (str): The name of the target file.

    Returns:
        tuple: A tuple containing a message (str) indicating error or success and a boolean value (bool).
               The boolean value is False if there are inconsistencies in the file or if it does not exist,
               and True if everything is in order.
    """

    validity = True
    message = ''
    try:
        empty_file = False
        extra_hashtag = False
        missing_hashtag = False
        invalid_character = False
        empty_line = False
        words_without_theme = False
        theme_without_words = False

        with open(target, 'r', encoding='utf-8') as file:
            if os.path.getsize(target) == 0:
                empty_file = True
            for line in file:
                hashtags = 0
                if line == '\n':
                    empty_line = True
                for char in line:
                    if char == '#':
                        hashtags += 1
                    if not char.isalpha() and char not in '- #,' and char != '\n':
                        invalid_character = True
                if hashtags > 1:
                    extra_hashtag = True
                if hashtags < 1 and not empty_line:
                    missing_hashtag = True
                if hashtags == 1:
                    checker = line.split('#')
                    if checker[0] == '':
                        words_without_theme = True
                    if checker[1] == '' or checker[1] == '\n':
                        theme_without_words = True

        if empty_file:
            message += 'Error: File "Biblio.txt" is empty.\n'
            validity = False
        if extra_hashtag:
            message += 'Error: Extra theme/words separator (#).\n'
            validity = False
        if missing_hashtag:
            message += 'Error: Missing theme/words separator (#).\n'
            validity = False
        if invalid_character:
            message += 'Error: Invalid character in the library.\n'
            validity = False
        if empty_line:
            message += 'Error: Empty line in the library.\n'
            validity = False
        if theme_without_words:
            message += 'Error: Theme without words.\n'
            validity = False
        if words_without_theme:
            message += 'Error: Words without a theme.\n'
            validity = False
        if validity:
            message += 'Library OK'

        return message, validity

    except FileNotFoundError:
        validity = False
        message += 'Error: File "Biblio.txt" not found.\n'
        return message, validity


class Game:  # Class containing the tools and execution of a game round
    
    def __init__(self, challenge):
        self.challenge = challenge  # Variable receiving a Challenge object
        self.attempts = 5  # Variable regulating user attempts
        self.hangman_stages = [
            "---------\n|/      |\n|\n|\n|\n|\n|\n --",
            "---------\n|/      |\n|       O\n|\n|\n|\n|\n --",
            "---------\n|/      |\n|       O\n|       ^\n|\n|\n|\n --",
            "---------\n|/      |\n|       O\n|       ^\n|       | \n|\n|\n --",
            "---------\n|/      |\n|       O\n|       ^\n|     / | \\ \n|       ^\n|\n --",
            "---------\n|/      |\n|       O\n|       ^\n|     / | \\ \n|       ^\n|     /   \\ \n --"
        ]  # Variable storing the visual elements of the hangman drawing
        self.hidden_word = challenge.generate_shadow()  # Variable receiving a list analogous to the word with underscores replacing the characters

    def game_start(self):  # Function that runs the game, checks remaining attempts, and displays/updates game visuals
        while True:
            print(self.hangman_stages[5 - self.attempts])
            print(f'Theme: {self.challenge.theme}')
            print(f'Total letters: {self.challenge.length}')
            self.print_word(self.hidden_word)
            letter = self.validate_guess()
            self.attempts += self.check_letter(letter, self.challenge, self.hidden_word)
            if self.attempts == 0:
                print(self.hangman_stages[5])
                print('YOU LOSE!')
                print(f'The word was: {self.challenge.word}')
                break
            if ''.join(self.hidden_word) == self.challenge.word:
                print('YOU WIN!')
                print(f'The word was: {self.challenge.word}')
                break

    @staticmethod
    def validate_guess():  # Function to validate player's guess, ensuring it is a single alphabetic character or hyphen
        while True:
            letter = input('Enter a letter: ')
            if len(letter) > 1:
                print('ENTER ONLY ONE LETTER!')
            if not letter.isalpha() and letter != '-':
                print('ENTER ONLY LETTERS OR HYPHEN (-)!')
            else:
                break
        letter = letter.lower()
        letter = unicodedata.normalize("NFD", letter)
        letter = letter.encode("ascii", "ignore")
        letter = letter.decode("utf-8")
        return letter
    
    @staticmethod
    def check_letter(letter, reference, target):  # Function to compare the guessed letter with the challenge word
        penalty = 0
        if letter in reference.reference:
            for i in range(0, len(reference.reference)):
                if letter == reference.reference[i]:
                    target[i] = reference.word[i]
        else:
            penalty = -1
        return penalty

    @staticmethod
    def print_word(word):  # Function to visually display the hidden_word to the player
        for char in word:
            print(f'{char}', end='')
        print('')


class Challenge:  # Class that generates a Challenge object with properties related to the word to be guessed
    
    def __init__(self, theme, word):
        self.word = word  # Receives the original word
        self.theme = theme  # Receives the theme of the word
        self.length = len(word.replace(' ', ''))  # Receives the length of the word excluding spaces
        self.reference = self.generate_reference(self.word)  # Receives the normalized word for comparison

    def generate_shadow(self):  # Function to generate a list analogous to the word, replacing characters with underscores except for spaces
        self.shadow = ['_'] * len(self.word)
        for i in range(len(self.word)):
            if self.word[i] == ' ':
                self.shadow[i] = ' '
        return self.shadow
    
    @staticmethod
    def generate_reference(word):  # Function to normalize a word to lowercase and remove accents for comparison
        comparator = word.lower()
        comparator = unicodedata.normalize('NFD', comparator)
        comparator = comparator.encode("ascii", "ignore")
        comparator = comparator.decode("utf-8")
        return comparator

class Database:  # Class to generate a word library from a text file for creating Challenge objects
    
    def __init__(self, file):
        self.database, self.database_keys = self.generate_database(file)

    def generate_challenge(self):  # Function that returns a Challenge object based on the generated library
        theme = random.choice(self.database_keys)
        word = random.choice(self.database[theme])
        return Challenge(theme, word)

    @staticmethod
    def generate_database(database_file):  # Function to open and read a text file to create a database dictionary and a list of themes
        with open(database_file, 'r', encoding="utf-8") as data:
            dictionary = {}
            themes = []
            for line in data:
                theme, words = line.split('#')
                words = words.replace('\n', '')
                words = words.split(',')
                dictionary[theme] = words
        
        for key in dictionary.keys():
            themes.append(key)
            
        return dictionary, themes
    
# Program

print("""
    ---------
    |/      |
    |       
    |     HANGMAN
    |        GAME
    |
    --""")

message, validity = check_file('Biblio.txt')
if validity:
    print(message)
    database = Database('Biblio.txt')
    while True:
        start = input('Do you want to start a new game? [Y/N] ').upper()
        if start not in 'YN':
            print('Enter only Y or N!')
        if len(start) > 1:
            print('Enter one option!')
        if start == "Y":
            challenge = database.generate_challenge()
            game = Game(challenge)
            game.game_start()
        if start == "N":
                print('Exiting the game!')
                time.sleep(3)
                exit()
else:
    print(message)
    print('Closing program...')
    time.sleep(5)
    exit()

# File "Biblio.txt" Requirements:
# The file must not be empty and must not contain blank lines.
# It should have themes with a corresponding list of words and vice versa.
# It should not contain non-alphabetic characters except for hashtag, commas, and spaces.
# Each line should contain a single theme and its respective list of words.
# The theme name should be announced first, followed by a # separator, then the list of words.
# Words within a theme should be separated by commas without any preceding or trailing spaces.

# General Program Functioning:
# The program will capture information from the text file and generate a database object.
# This object will then create a challenge object containing the word, its theme, and other related information.
# The theme and word are chosen randomly from the database.
# The challenge object is provided as a parameter to a game object, responsible for executing a game round.
# A new game object is created whenever a new game is desired.
# The program will terminate if a known error occurs during database generation, informing the user of any existing errors.
# If no errors are found, the program initiates a loop, asking the user if they want to start a new game.
# The question can only be answered with "Y" for yes and "N" for no.
# If the answer is "Y," a game is executed, and at the end, a victory or defeat message is displayed.
# The loop restarts, asking the question again and generating new games as long as the user answers "Y."
# Upon answering "N," the program displays a closing message and terminates.
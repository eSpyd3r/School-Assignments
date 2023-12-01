#Author: Ethan Lim 261029610

import wordle_utils as word
import random

wordle_word_length = 5
max_num_of_guesses = 6
char_green = '\x1b[6;30;42m'
char_yellow = '\x1b[6;30;43m'
char_gray =  '\x1b[6;30;47m'
char_end =  '\x1b[0m'

def is_valid_word(word, word_list):
	""" (str, list) -> bool
	Returns True or False depending on if word is in word_list
	

	>>> is_valid_word('about', ['abounds', 'about', 'abouts', 'above', 'aboveboard'])
	True

	>>> is_valid_word('abou', ['abounds', 'about', 'abouts', 'above', 'aboveboard'])
	False

	>>> is_valid_word('About', ['abounds', 'about', 'abouts', 'above', 'aboveboard'])
	True

	"""
	word = word.lower()

	if word in word_list and len(word) == 5: #word is only valid if it is found in the dictionary word_list and is of len 5
		return True

	else:
		return False


def print_string_list(word_list):
	""" (list) -> str
	Prints each string in the list on a new line

	>>> print_string_list(['abounds', 'about', 'abouts', 'aboveboard', 'abovedeck'])
	abounds
	about
	abouts
	aboveboard
	abovedeck


	>>> print_string_list(['word', 'worth', 'words', 'worry', 'wonder'])
	word
	worth
	words
	worry
	wonder

	>>> print_string_list(['class', 'classes', 'classified', 'clash', 'classic'])
	class
	classes
	classified
	clash
	classic

	"""

	for word in word_list: #prints each index of the list, line by line
		print(word)


def color_string(word, color):
	"""(str, str) -> str
	Returns colored word

	>>> color_string('about', 'green')
	'\x1b[6;30;42mabout\x1b[0m

	>>> color_string('word', 'gray')
	\x1b[6;30;47mword\x1b[0m

	>>> color_string('class', 'orange')
	Invalid color.
	class
	"""

	color = color.lower()

	if color == "green": #for each color, word is surrounded by char_color and char_end
		colored_word = char_green + word + char_end

	elif color == "gray":
		colored_word = char_gray + word + char_end

	elif color == "yellow":
		colored_word = char_yellow + word + char_end

	elif color not in ['green', 'gray', 'yellow']: #list of valid colors
		print("Invalid color.")
		colored_word = word

	return colored_word

def get_all_5_letter_words(all_word_list):
	"""(list) -> list
	Returns list of words that are of wordle_word_length characters long

	>>> get_all_5_letter_words(['abs', 'about', 'abouts', 'above', 'aboveboard', 'aloft'])
	['about', 'above', 'aloft']

	>>> get_all_5_letter_words(['class', 'classes', 'classified', 'clash', 'classic'])
	['class', 'clash']

	>>> get_all_5_letter_words(['word', 'worth', 'words', 'worry', 'wonder'])
	['worth', 'words', 'worry']
	"""
	wordle_list = []

	for word in all_word_list:
		if len(word) == wordle_word_length: #Every index in all_word_list that is of len 5 is added to wordle_list
			wordle_list.append(word)

	return wordle_list


def choose_mode_and_wordle(wordle_list):
	"""(list) -> str
	Returns the 'wordle' of the game

	>>> random.seed(20)
	>>> choose_mode_and_wordle('about', 'above', 'aloft', 'aeons'])
	Enter the number of players: 1
	'above'

	>>> choose_mode_and_word(wordle_list)

	Enter the number of players: 2

	***** Player 1's turn. ***** 
			Input today's word: #this is masked after Player 1 inputs answer
                                                                  

	***** Player 2's turn. ***** 
	
	# input from player 1 is returned


	>>> choose_mode_and_wordle(wordle_list) #wordle_list is the list of all 5 words in the provided dictionary
	Enter the number of players: 1

	*random word* # unless seed is provided, this should be random each time
	"""

	while True:
		mode = int(input("Enter the number of players: "))
		
		if mode == 1:
			wordle = generate_random_wordle(wordle_list) #generates random wordle for 1 player
			break
		elif mode == 2:
			print("\n***** Player 1's turn. ***** \n" )

			wordle = input_wordle(wordle_list) #input_wordle ensures that the input from player 1 is valid

			print("\n***** Player 2's turn. ***** \n" )

			break	
		else:
			print("Wordle can be played with 1 or 2 players. Please only enter 1 or 2. ")

	return wordle


def input_wordle(word_list):
	"""(list) -> str
	Returns wordle if found in list
	"""


	while True:
		wordle = word.input_and_hide("Input today's word: ")
		wordle = wordle.lower() #resolves case sensitivity

		if wordle in word_list:
			break
		else:
			print("Not a valid word, please enter a new one. ") #loop continues if word isn't valid

	return wordle

def generate_random_wordle(wordle_list):
	"""(list) -> str
	Returns random wordle in word_list

	>>> random.seed(100)
	>>> generate_random_wordle(['about', 'above', 'aloft', 'aeons'])
	'above'

	>>> generate_random_wordle(['crane', 'chase', 'cache', 'canes'])
	'crane'

	>>> generate_random_wordle(['crane', 'chase', 'cache', 'canes'])
	'cache'


	"""
	rand_index = random.randint(0, len(wordle_list)) #random integer is generated that represents an index of wordle_list
	wordle = wordle_list[rand_index]

	return wordle

def play_with_word(wordle, wordle_list):
	"""(str, wordle_list) -> int
	Initiates "guessing" of the game and returns the number of guesses taken

	>>> play_with_word('drink', wordle_list) #wordle_list is the whole lsit of 5 letter words

	Enter a guess: dRiNk
	drink #all letters green

	1 #returns number of tries

	>>> play_with_word('apple', ['apple', 'drink', 'arose', 'lakes'])

	Enter a guess: drink
	drink					#all letters gray
	Enter a guess: arose
	drink					#all letters gray
	arose					#'a' and 'e' green
	Enter a guess: lakes
	drink					#all letters gray
	arose					#'a' and 'e' green	
	lakes					#'l' and 'a' and 'e' yellow
	Enter a guess: apple
	drink					#all letters gray
	arose					#'a' and 'e' green	
	lakes					#'l' and 'a' and 'e' yellow
	apple					#all letters green

	4 #returns number of tries

	>>> play_with_word('apple', ['apple', 'drink', 'arose', 'lakes'])

	Enter a guess: drink
	drink					#all letters gray
	Enter a guess: drink
	drink					#all letters gray
	drink					#all letters gray
	Enter a guess: drink
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	Enter a guess: drink
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	Enter a guess: drink
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	Enter a guess: drink
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray
	drink					#all letters gray

	7 #returns 7 after 6 tries, since maximum number of guesses has been reached

	"""
	number_of_tries = 1
	colored_guess = []
	
	for attempt in range(max_num_of_guesses):
		while True: #loops until valid guess
			guess = input("Enter a guess: ")
			guess = guess.lower()

			if guess not in wordle_list: #checks if guess is valid
				print("Not a valid word, please enter a new one. ")
				continue

			colored_guess.append(compare_and_color_word(guess, wordle)) #adds colored guess if the guess is valid
			print_string_list(colored_guess) #prints the list of valid guesses already made

			break #loops ends once valid guess is made

		if guess == wordle:
			break

		number_of_tries += 1 #number of tries is only added if the guess is valid and NOT the wordle

		
	return number_of_tries


def compare_and_color_word(guess, wordle):
	"""(str, str) -> str
	Returns colored word, depending on the guess and the wordle

	>>> compare_and_color_word('drink', 'apple')
	drink #all leters gray'

	>>> compare_and_color_word('arose', 'apple')
	arose #'a' and 'e' green while 'ros' gray

	>>> compare_and_color_word('AROSE', "APPLE')
	AROSE #'A' and 'E' green while 'ROS' gray #resolving case sensitivity doesn't occur here
	"""
	colored_word = ""

	for i in range(wordle_word_length):
		if wordle[i] == guess[i]: #only returns green character if the index in guess and wordle are the same letter
			colored_word += color_string(guess[i], "green")
		elif guess[i] in wordle and wordle[i] != guess[i]: #only returns yellow if the the same character is found in wordle but is not of the same index
			colored_word += color_string(guess[i], "yellow")
		else: #only returns gray if the character is not found in wordle
			colored_word += color_string(guess[i], "gray")

	return colored_word


def print_final_message(number_of_tries, wordle):
	"""(int, str) -> None
	Prints final message, either the number of guesses to solution or revealing the correct answer
c
	>>> print_final_message(3, 'about')
	You won! It took you 3 guesses.

	>>> print_final_message(7, 'cache')
	You lost! The word was cache #with all letters of cache green

	>>> print_final_message(1, 'about')
	You won! It took you 1 guess
	"""

	if number_of_tries == 1: #specific case for guesssing on first try
		print("You won! It took you 1 guess.")

	elif number_of_tries < (max_num_of_guesses + 1): #only executes if the number of tries to solution is less than 7 (max + 1)
		print("You won! It took you " + str(number_of_tries) + " guesses.")

	else:
		solution = color_string(wordle, "green") #prints solution if 6 guesses are made
		print("You lost! The word was " + solution)

def play(wordle_list):
	"""(list) -> None
	Collects wordle and plays game
	"""

	wordle = choose_mode_and_wordle(wordle_list) #collects wordle and determines if there are 1 or 2 players

	number_of_tries = play_with_word(wordle, wordle_list) #collects number of tries by executing the "playing" part of the program

	print_final_message(number_of_tries, wordle) #once the playing is finished, the final message is printed

def main():
	"""(None) -> None
	Calls helper functions and 'play' function to make the game whole
	"""
	all_words = word.load_words() #gathers all words
	wordle_list = get_all_5_letter_words(all_words) #gathers all 5 letter words form all_words that can be used for the game

	play(wordle_list) #playing with wordle_list words

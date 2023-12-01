#author: Ethan Lim 261029610

import random
import pickle

def replace(string, char, index):
	"""(str, str, int) -> str
	Returns string with the first character of the original replaced

	"""
	return string[:index] + char + string[index + 1:]

def get_punctuation_index(string, symbols):
	""" (str) -> int
	Returns the index of the first detected use of a period, question mark, or exclamation

	"""
	index = 0

	for char in string:
		if char in symbols:
			break
		index += 1

	return index

def capitalize_sentences(sentence):
	"""(str) -> str
	Retruns string that capitalizes the first letter of every sentence in the original stirng

	>>> capitalize_sentences("hello. hello! hello???? HI!")
	'Hello. Hello! Hello???? HI!'

	>>> capitalize_sentences("!wHaT")
	'!wHaT'

	>>> capitalize_sentences("1 is nOt one")
	'1 is nOt one'
	"""
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	sentence_end = "!?."

	words = sentence.split() #splits string into list format
	cap_words = []
	caps = False

	if words[-1][-1] in sentence_end:
		caps = True
	for each_word in words:
		if each_word.isupper():
			caps = False

		if each_word[0] in alphabet and caps: #will capitalize if the first letter is part of the regular alphabet AND caps is True
			first_letter = each_word[0]
			first_letter = first_letter.upper()
			word = replace(each_word, first_letter, 0)
			cap_words.append(word) #capitalized words are added to a separate list
			caps = False

		else:
			cap_words.append(each_word)
			caps = False

		if each_word[-1] in sentence_end:
			caps = True

	new_sentence = " ".join(cap_words)

	return new_sentence


def capitalize_sentence_grid(various_phrases):
	"""(list) -> list
	Returns a nested list with each letter at the beginning of each sentence capitalized when combining the lists
	
	>>> grid = [["you", "might", "think"], ["these", "are", "separate", "sentences"], \
			["but", "they", "are", "not!", "ok,", "this"], ["one", "is."]]
	
	>>> capitalize_sentence_grid(grid)
	[['You', 'might', 'think'], ['these', 'are', 'separate', 'sentences'], ['but', 'they', \
	'are', 'not!', 'Ok,', 'this'], ['one', 'is.']]

	>>> grid = [["you", "might", "think"], ["these", "are", "separate", "sentences"], \
			["but", "they", "are", "not!", "ok,", "this"], ["one", "is."]]
	
	>>> capitalize_sentence_grid(grid)
	[['You', 'might', 'think.'], ['These', 'are', 'separate', 'sentences'], ['but', 'they', \
	'are', 'not!', 'Ok.', 'This.'], ['One', 'is.']]

	>>> grid = [["you", "might", "think"], ["these", "are", "separate", "sentences"], \
			["but", "they", "are", "not!", "ok,", "this"], ["one", "is."]]
	
	>>> capitalize_sentence_grid(grid)
	[['You', 'might', 'think'], ['these', 'are', 'separate.', 'Sentences.'], ['But', 'they', \
	'are', 'not!', 'Ok,', 'this'], ['one', 'is.']]
	"""
	sentence_end = "!?."
	cap_grid = []
	cap_first = True
	cap_def = False


	for phrase in range(0,len(various_phrases)):
		if phrase != 0 and various_phrases[phrase-1][-1][-1] in sentence_end:
			cap_first = True #checks if the first letter of the phrase is going to be caps, dedpening on the end of the last phrase

		if cap_first: #if the first letter needs to capitalized, it's the start of a new sentence
			edit_phrase = " ".join(various_phrases[phrase])
			edit_phrase += "." #adds end punctuation to the end; causes capitalization of the first word

			cap_phrase = capitalize_sentences(edit_phrase)
			cap_phrase = cap_phrase[0:len(cap_phrase)-1].split() #packs into list, omitting the period added earlier

			cap_grid.append(cap_phrase)

			cap_first = False

			continue
		
		edit_phrase = " ".join(various_phrases[phrase])

		for char in range(0, len(edit_phrase)):
			if edit_phrase[char] in sentence_end and char != (len(edit_phrase)-1): #if end punctuation is found ANYWHERE in the middle, capitalization must occur
				cap_def = True
				break
	
			elif edit_phrase[char] in sentence_end and char == (len(edit_phrase)-1):
				cap_def = False #if there is no end punctuation in the middle, but only at the end, capitalization doesn't need to occur
				
		if cap_def:
			delete_last = False

			if edit_phrase[-1] not in sentence_end: #since capitalizing is taking place, words after end punctuation need to be capitalized
				edit_phrase += "."
				delete_last = True #will delete the added period

			cap_phrase = capitalize_sentences(edit_phrase[get_punctuation_index(edit_phrase, sentence_end)+1:])

			if delete_last: #will delete the added period
				cap_phrase = edit_phrase[0:get_punctuation_index(edit_phrase, sentence_end)+1] + " " + cap_phrase[0:len(cap_phrase)-1]
			else:
				cap_phrase = edit_phrase[0:get_punctuation_index(edit_phrase, sentence_end)+1] + " " + cap_phrase
			
			cap_phrase = cap_phrase.split()
			cap_grid.append(cap_phrase)

		else: #capitalization is not needed, so nothing happens to the original phrase
			cap_grid.append(various_phrases[phrase])




	return cap_grid



def fill_in_madlib(sentence, word_dict):
	"""(str, dict) -> str
	Returns a string that is a completed/filled version of the original, using words from the dictionary

	>>> random.seed(2022)

	>>> d = {'PAST-TENSE-VERB': ['pondered', 'scribbled', 'snoozled', 'studied'], 'ADJECTIVE': ['dreamy', 'weak', 'weary', 'starry', 'lazy']}

	>>> fill_in_madlib("Once upon a midnight [ADJECTIVE_1], while I [PAST-TENSE-VERB], [ADJECTIVE_2] and [ADJECTIVE_3],", d)
	'Once upon a midnight lazy, while I snoozled, starry and weary,'

	>>> d = {'PAST-TENSE-VERB': ['pondered', 'scribbled', 'snoozled', 'studied'], 'ADJECTIVE': ['dreamy']}

	>>> fill_in_madlib("Once upon a midnight [ADJECTIVE_1], while I [PAST-TENSE-VERB], [ADJECTIVE_2] and [ADJECTIVE_3],", d)
	"AssertionError: There are not enough words in the dictionary to complete the string."

	>>> d = {'PAST-TENSE-VERB': ['pondered', 'scribbled', 'snoozled', 'studied'], 'ADJECTIVE': ['dreamy', 'weak', 'weary', 'starry', 'lazy']}

	>>> fill_in_madlib(2, d)
	"AssertionError: The provided sentence is not a string."

	>>> fill_in_madlib("Once upon a midnight [ADJECTIVE_1], while I [PAST-TENSE-VERB], [ADJECTIVE_2] and [ADJECTIVE_3]", 2)
	"AssertionError: The provided 'dictionary' of words is not a dictionary."

	>>> d = {'PAST-TENSE-VERB': ['pondered', 'scribbled', 'snoozled', 'studied'], 'ADJECTIVE': ['dreamy', 'weak', 'weary', 'starry', 'lazy']}

	>>> fill_in_madlib("Once upon a midnight [VERB], while I [PAST-TENSE-VERB], [ADJECTIVE_2] and [ADJECTIVE_3],", d)
	"AssertionError: A word type found in the string is not found in the dictionary"
	
	>>> d = {2: ['pondered', 'scribbled', 'snoozled', 'studied'], 'ADJECTIVE': ['dreamy', 'weak', 'weary', 'starry', 'lazy']}

	>>> fill_in_madlib("Once upon a midnight [VERB], while I [PAST-TENSE-VERB], [ADJECTIVE_2] and [ADJECTIVE_3],", d)
	"AssertionError: The type for 1 or more of the keys in the dictionary are not of type 'str'."

	>>> random.seed(2022)

	>>> d = {'TIME': ['an eternity', 'a few hours', 'all day'], 'ADJECTIVE': ['INSANE', 'small', 'large'], "EMOTION": ['happy', 'sad', 'excited', 'annoyed']}

	>>> fill_in_madlib("I have a(n) [ADJECTIVE] amount of homework. The homework will take me [TIME] to finish. I am so [EMOTION]!", d)
	"I have a(n) large amount of homework. The homework will take me a few hours to finish. I am so annoyed!"

	>>> random.seed(2022)

	>>> d = {'ADJECTIVE': ['quick', 'quickly', 'quickest', 'more quickly']}

	>>> fill_in_madlib("[ADJECTIVE_1] [ADJECTIVE_2] [ADJECTIVE_3]", d)
	"quickest more quickly quick"
	"""

	if type(sentence) != str:
		raise AssertionError("The provided sentence is not a string.") #edge case in which the input sentence is not a string

	if type(word_dict) != dict:
		raise AssertionError("The provided 'dictionary' of words is not a dictionary.") #edge case in which the input 'dictionary' is not of type dict

	for key in word_dict:
		if type(key) != str:
			raise AssertionError("The type for 1 or more of the keys in the dictionary are not of type 'str'.") #edge case in which the type for a key is not a string
		if type(word_dict[key]) != list:
			raise AssertionError("A value for 1 or more keys in the dictionary are not of type 'list'") #edge case in which a value for a key is not of type list

	word_types = []
	non_word_symbols = "[_],!?."
	numbers = "1234567890"


	sentence_as_list = sentence.split() #packs string into list
	sentence_as_enumerate = enumerate(sentence_as_list) #breaks list into tuples

	for tup in sentence_as_enumerate:
		for item in tup:
			if item in word_types or type(item) != str: #since one of the elements in the tuple will be an int
				continue
			if '[' in item: #some of the strings in the tuples will be words we don't need to replace
				word_types.append(item[0:get_punctuation_index(item, "]") + 1]) 

	words_selected = []
	key_type_list = []

	for each_type in word_types: #iterates though each type needed; needed to choose a word from a specific key
		key_type = ""
		for letter in each_type:
			if letter in non_word_symbols or letter in numbers: #we only need the key type (e.g. ADJECTIVE or VERB w/o the brackets, underscores, or numbers)
				continue
			else:
				key_type += letter

		key_type_list.append(key_type) #adds the key type to a new list
		num_of_same_type = key_type_list.count(key_type)

		if num_of_same_type > len(word_dict.get(key_type)): #checks if there are enough words to fill in the needed blanks in the original sentence
			raise AssertionError("There are not enough words in the dictionary to complete the string.")

		while True:
			if key_type not in word_dict: #checks if the original string needs a word type that is not provided by the dictionary
				raise AssertionError("A word type found in the string is not found in the dictionary")
			else:
				chosen_word = random.choice(word_dict.get(key_type)) #chooses random word from a word_type key-value

			if chosen_word not in words_selected: #if the word hasn't been used it, it is added to a list to track which words have been used
				words_selected.append(chosen_word)
				break #the chosen word will proceed to be used in the given string if the word hasn't been chosen from the same keyValue

		sentence = sentence.replace(each_type, chosen_word)

	return sentence

def load_and_process_madlib(file):
	"""(str) -> none
	Reads madlib string and dictionary from 2 different files, and fills in the madlib string using the words provided by the dicitonary
	
	>>> random.seed(2022) #dictionary in pkl is {'PAST-TENSE-VERB': ['pondered', 'scribbled', 'snoozled', 'studied'], 'ADJECTIVE': ['dreamy', 'weak', 'weary', 'starry', 'lazy']}

	>>> load_and_process_madlib('madlib1.txt') #file contains "Once upon a midnight [ADJECTIVE_1], while I [PAST-TENSE-VERB], [ADJECTIVE_2] and [ADJECTIVE_3],"

	>>> f = open('madlib1_filled.txt', 'r') 

	>>> s = f.read()

	>>> s
	'Once upon a midnight lazy, while I snoozled, starry and weary,'

	>>> random.seed(2022) #dictionary in pkl is {'ADJECTIVE': ['quick', 'quickly', 'quickest', 'more quickly']}

	>>> load_and_process_madlib('madlib1.txt') #file contains "[ADJECTIVE_1] [ADJECTIVE_2] [ADJECTIVE_3]"

	>>> f = open('madlib1_filled.txt', 'r')

	>>> s = f.read()

	>>> s
	'quickest more quickly quick'

	>>> random.seed(2022) #dictionary in pkl is {'ADJECTIVE': ['quick', 'quickly']}

	>>> load_and_process_madlib('madlib1.txt') #file contains "[ADJECTIVE_1] [ADJECTIVE_2] [ADJECTIVE_3]"

	>>> f = open('madlib1_filled.txt', 'r')

	>>> s = f.read()

	>>> s
	AssertionError: There are not enough words in the dictionary to complete the string.
	"""

	pkl = open("word_dict.pkl", "rb")
	word_dict = pickle.load(pkl) #reads contents of pickle file containing dictionary
	pkl.close()

	fobj = open(file, "r")
	mad_lib_string = fobj.read() #reads contents of the file containing the madlib string
	fobj.close()

	mad_lib = fill_in_madlib(mad_lib_string, word_dict)

	new_file_name = file[0:get_punctuation_index(file, ".")] + '_filled.txt' #makes a new file with '_filled' added to the original file name (before type)

	mad_lib_obj = open(new_file_name, 'w')
	mad_lib_obj.write(mad_lib) #writes to the new file
	mad_lib_obj.close()

def generate_comment():
	"""(none) -> str
	Returns filled madlib that was written to madlibk_filled.txt

	>>> random.seed(2022)
	
	>>> generate_comment()
	'Elsa Ifstatement aided me with exams. Elsa Ifstatement better win!'

	>>> random.seed(1999)

	>>> generate_comment()
	'I am exhausted! Can't this election be over already? It's been forever!'

	>>> random.seed(202)

	>>> generate_comment()
	'Who would've thought that Dee Buh-Ger would run in this year's election? Epecially after they won last year!'

	"""

	madlib_k = str(random.randint(1, 10))
	mad_libk_file = 'madlib' + madlib_k + '.txt' #chooses random file by randomizing 'k'

	load_and_process_madlib(mad_libk_file) #loads pkl dictionary and initiates 'madlibbing' on file mad_libk_file

	mad_libk_filled_file = 'madlib' + madlib_k + '_filled' + '.txt'

	mad_libk_obj = open(mad_libk_filled_file, 'r') #reads finished mad lib in mad_libk_filled_file
	mad_libk_string = mad_libk_obj.read()
	mad_libk_obj.close()

	return mad_libk_string 



if __name__ == "__main__":
	word_dict = {'CANDIDATE': ['Bool Ian', 'Alex Thonny', 'Elsa Ifstatement', 'Dee Buh-Ger'], 'NEGATIVE-PAST-TENSE-VERB': ['did not help', 'forgot to help', 'scammed'], \
	'ASSIGNMENT': ['Assignment 1', 'Assignment 2', 'exams', 'midterms'], 'NEGATIVE-NOUN': ['jerk', 'moron', 'scumbag'], 'POSITIVE-PAST-TENSE-VERB': ['helped', 'aided', 'started'], \
	'MCGILL-PROF': ['Professor Campbell', 'Professor Ragan', 'Professor Trudeau', 'Professor Hendry'], 'CANDIDATE-EVENT': ['escaped prison', 'ran last year', 'failed middle-school', 'won last year'], \
	'OTHER-PERSON-DIRECTED-EMOTION': ['liked', 'hated', 'disliked', 'loved'], 'STATE-OF-BEING': ['die', 'run-away', 'get lost', 'go missing'], 'ADJECTIVE': ['funny', 'stupid', 'hilarious', 'cringy', 'strange', 'random'], \
	'MCGILL-LOCATION': ['Redpath Library', 'The Roddick Gates', 'Molson Stadium', 'The Fitness Centre'], 'PERSON-ADJECTIVE': ['Mega', 'Big', 'One-and-Only', 'Impressive'], 'OUTCOME': ['win', 'lose'], \
	'EMOTION': ['anxious', 'stressed', 'exhausted', 'ready'], 'LONG-TIME': ['years', 'forever', 'weeks', 'ages']}

	save_pkl = open("word_dict.pkl", "wb")
	pickle.dump(word_dict, save_pkl)
	save_pkl.close()


	
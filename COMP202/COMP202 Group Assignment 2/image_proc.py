#author: Ethan Lim

def invert(image):
    """(str) -> str
    Returns inverted image string

    >>> invert('0111')
    '1000'

    >>> invert('1000')
    0111

    >>> invert('101010101')
    010101010
    """

    image = str(image)
    inverted_bin_num = ''

    for i in image:

        if i == '0': #checks if i in image = string 'O'
            inverted_bin_num += '1' #adds string '1' to inverted lsit
        else: #in this case, if i != -, i == 1
            inverted_bin_num += '0' #adds string '0' to inverted list

    return inverted_bin_num


def flip_horizontal(image, height, width):
	""" (str, int, int) -> str
	Flips image string horizontally

	>>> flip_horizontal('011100', 2, 3)
	'110001'

	>>> flip_horizontal('100101', 3, 2)
	011010

	>>> flip_horizontal('0110', 4, 1)
	0110
	"""

	image = str(image)
	hold_string = ''
	horizontal_image = ''

	for i in range(int(len(image)/width)): #runs enough times to complete the final string image
		hold_string = (image[i*width:(i+1)*width]) #holds temporary value/string for each iteration
		horizontal_image += hold_string[::-1] #adds temporary value to the 'saved' string

	return horizontal_image


def flip_vertical(image, height, width):
	""" (str, int, int) -> str
	Flips image string vertically

	>>> flip_vertical('011100', 2, 3)
	'100011'

	>>> flip_vertical('10010111', 4, 2)
	'11010110'
	

	>>> flip_vertical('0110', 2, 2)
	'1001'
	"""

	image = str(image)
	hold_string = ''
	vertical_colns= ''
	vertical_image = ''

	for i in range(width): #runs enough times to complete the final string image
		for n in range(height):
			hold_string += image[n*width+i]

		vertical_colns += hold_string[::-1]
		hold_string = ""
	
	for z in range(height):
		for m in range(width):
			vertical_image += vertical_colns[(m*height)+z]

	return vertical_image


def crop(image, height, width, x_colm, y_row, crop_height, crop_width):
	""" (str, int, int, int, int, int, int) -> str
	Returns image cropped to a certain rectangle size

	>>> crop('000111000', 3, 3, 1, 1, 2, 2)
	'1100'

	>>> crop('0001110001', 2, 5, 2, 0, 2. 3)
	'011001'


	>>> crop('110010', 3, 2, 0, 1, 1, 2)
	'00'

	"""
	crop_image = ""

	for h in range(crop_height): #crop_height determines amount of rows to parse
		for w in range(crop_width): #parses to the length of the crop_width
			crop_image += image[(h * width) + (y_row * width) + x_colm + w] #DOESN'T WORK IF x_col and y_row START AT IMPOSSIBLE PLACE

	return crop_image

def find_end_of_repeated_substring(s, i, c):
	""" (str, int, str) -> int
	Returns the index of the last consecutive occurrencce of 'c'

	>>> find_end_of_repeated_substring('011', 1, '1')
	2

	>>> find_end_of_repeated_substring('abaaaaaab', 0, 'a')
	0

	>>> find_end_of_repeated_substring('abaabaabaab', 5, 'a')
	6
	"""
	count_from_i = 0

	for char in s[i + 1:]: #i + 1 because, if there are no consecutive characters, i = initial i.
		if char == c:
			i += 1 #adds to the index value for every consecutive character
			continue

		break #stops loop once the condition above isn't met

	return i

def compress(image):
	""" (str) -> str
	Returns compressed image string

	>>> compress('00010111111111111111000111111')
	'0 3 1 1 2'

	>>> compress('10')
	'1 1 1'

	>>> compress('0')
	'0 1'
	"""
	compressed_image = "" #empty string to hold the compressed image
	compressed_image += image[0] 

	track_index = 0
	index_in_string = 0

	while track_index < len(image): #iterates enough times to cover the length of the original string
		num_of_consec = find_end_of_repeated_substring(image, index_in_string, image[index_in_string]) + 1 - index_in_string #number of conecutive 1s or 0s
		compressed_image += " " + str(num_of_consec) #adds num_of_consec as a string to the compressed image string

		index_in_string += num_of_consec #'saves' the index where find_end_of_repeated_substring() left off

		track_index += num_of_consec

	compressed_image += " "

	for char in image:
		if char not in ['0', '1', ' ']:
			compressed_image = ""

	return compressed_image[:-1]

def decompress(compressed_image):
	""" (str) -> str
	Returns decompressed compressed-image string
	
	>>> decompress('0 3 1 1 8')
	'0001011111111'

	>>> decompress('0 2')
	'00'

	>>> decompress('1 10')
	'1111111111'	
	"""
	decompressed_image = ""
	num_count = 1
	index = 2
	num_in_string = 1
	current_num = compressed_image[0]
	check = True

	for char in compressed_image:
		if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']:
			decompressed_image = ""
			check = False

	
	for amount_num in compressed_image: #counts the number of numbers (not indexes)
		if amount_num == " ":
			num_in_string += 1

	if check:
		compressed_image += " " #re-appends space to the end of the compressed string: allows for loop to complete to last number
	while check:	
		multiplier = "" #resets multiplier to null after each iteration of while loop
		for num in compressed_image[index:]:
			if num == " ":
				index += 1 #at the end of each while loop iteration, the location of the parse in for loose is kept
				num_count += 1
				break 
			else:
				index += 1
				multiplier += num
				
		decompressed_image += current_num * int(multiplier) #adds consecutive digits to decompressed string

		if num_count == num_in_string: #while loop breaks once all numbers (not indexes) parse
			break

		if current_num == "1": #alternates between 0 and 1 as the conescutive number
			current_num = "0"
		else:
			current_num = "1"

	return decompressed_image

def process_command(cmd_string, image, height, width):
	"""(str, str, int, int) -> str
	Retruns modified image string

	>>> process_command()

	>>> process_command()

	>>> process_command()
	"""
	index = 0
	call_count = 0
	func_start = 0
	cmd_string += " "
	
	cmd_count = 0
	for space_count in cmd_string:
		if space_count == " ":
			cmd_count += 1

	cr_index = 3
	cr_int_count = 0
	cr_int_start = 0

	while True:
		index = func_start
		for cmd in cmd_string[index:]:
			index += 1

			if cmd == " ":
				func_to_call = cmd_string[func_start:index] #collects the characters that refer to specific helper function
				func_start = index
				break
		if func_to_call == "INV ":
			image = invert(image)
			call_count += 1
		elif func_to_call == "FH ":
			image = flip_horizontal(image, height, width)
			call_count += 1
		elif func_to_call == "FV ":
			image = flip_vertical(image, height, width)
			call_count += 1
		elif func_to_call == "DC ":
			image = decompress(image)
			call_count += 1
		elif func_to_call == "CP ":
			image = compress(image)
			call_count += 1
		elif "CR" in func_to_call:
			func_to_call += ","
			while True: #similar to overall function, as this specific case refers to further identifying of integers/characters
				cr_index = cr_int_start
				for cr_int in func_to_call[cr_index:]:
					cr_index += 1
					if cr_int == ",":
						cr_int_count += 1
						cr_num = func_to_call[cr_int_start:cr_index]
						cr_int_start = cr_index + 1
						break

				if cr_int_count == 1: #since the paramaters of crop are also in the same position of the initial string, these conditionals always remain true
					x_colm = cr_num
				elif cr_int_count == 2:
					y_row = cr_num
				elif cr_int_count == 3:
					crop_height = cr_num
				elif cr_int_count == 4:
					crop_width = cr_num
					image = crop(image, height, width, x_colm, y_row, crop_height, crop_width) #finally calls the crop function once all of the integers are collectied
					break

			call_count += 1 

		if call_count == cmd_count:
			break

	return image
#Author: Ethan Lim 261029610

import random

def roll_die():
	"""(noneType) -> int
	Randomly generates a number between 1 and 6, like a die

	>>> roll_die()
	1

	>>> roll_die()
	5

	>>> roll_die()
	6
	"""
	roll = random.randint(1,6) #like a normal die, 6 random possibilities of integers

	return roll

def is_available(building, room_num, time):
	"""(str, str, int) -> bool
	Returns the availability of a room in the McLennan or Redpath Library at a specified time

	>>> is_available("Redpath", "R2-14", 11)
	False

	>>>	is_available("Redpath", "Floor 2 Pod 1", "13")
	False

	>>> is_available("Macdonald Campus Lib", "201", "10")
	True
	"""

	building = building.lower() #removing case sensitivity

	if building == "mclennan" or building == "redpath" or time not in range(8, 12): #conditions for unavailability
		available = False

	else: #any other building and within range (8,13) hours
		roll1 = roll_die()
		roll2 = roll_die()
		roll3 = roll_die()
		roll_sum = roll1 + roll2 + roll3

		if roll_sum <= 5: #possible that the above conditions are met, but not the dice roll
			available = True

		else:
			available = False

	return available

def find_available():
	"""(noneType) -> noneType
	Promts user to input values for is_available and displays the number of attempts

	>>> find_available()
	Building to check: mClenNan
	Room number in mClenNan: 201
	Hour between 1h and 24h: 10

	Room Unavailable. Try again
	Building to check: rEdPaTh
	Room number in rEdPaTh: 201
	Hour between 1h and 24h: 11

	Room Unavailable. Try again
	Building to check: c4
	Room number in c4: 201
	Hour between 1h and 24h: 1

	Room Unavailable. Try again
	Building to check: c4
	Room number in c4: 201
	Hour between 1h and 24h: 11

	This room is available at this time. Here's how many attempts it took: 4

	>>> find_available()
	Building to check: Macdonald Campus Library
	Room number in Macdonald Campus Library: 201
	Hour between 1h and 24h: 7

	Room Unavailable. Try again
	Building to check: Macdonald Campus Library
	Room number in Macdonald Campus Library: 201
	Hour between 1h and 24h: 8

	Room Unavailable. Try again
	Building to check: Macdonald Campus Library
	Room number in Macdonald Campus Library: 201
	Hour between 1h and 24h: 8

	This room is available at this time. Here's how many attempts it took: 3

	>>> find_available()
	Building to check: ;skadjfas;ldkjf
	Room number in ;skadjfas;ldkjf: 201
	Hour between 1h and 24h: 12

	This room is available at this time. Here's how many attempts it took: 1
	"""
	check = True
	tries = 1 #first attempt will be first try
	
	while check:
		building = str(input("Building to check: "))
		room_num = str(input("Room number in " + building + ": "))
		time = int(input("Hour between 1h and 24h: "))

		available = is_available(building, room_num, time)

		if available: 
			print("\nThis room is available at this time. Here's how many attempts it took:", tries)
			break #stops asking and counting once available room is found

		else: #adds to counter and continues to prompt user if room is unavailable
			print("\nRoom Unavailable. Try again")
			tries += 1 #if the room is unavailable, tries counter increases by 1 and runs again



find_available()




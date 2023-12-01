#Author: Ethan Lim 261029610

MILES_PER_HOUR = 60.0
MILES_PER_GALLON = 30.0 
MINUTES_PER_HOUR = 60.0
KILOMETRES_PER_MILE = 25146 / 15625


def ask_question(question, option1, option2, option3, option4): 
    """ (str, str, str, str, str) -> str
    Retruns the user's input as string

    >>> user_respone = ask_question('Which color is your favorite?', 'red', 'lime', 'blue', 'gray')

    Which color is your favorite?
    1 red
    2 lime
    3 blue
    4 gray
    Your answer: 4
   
    >>> print(user_response)
    4

    >>>  user_response = ask_question('Do you like soccer?', 'yes', 'no', '', '')
    
    Do you like soccer?
    1 yes
    2 no
    Your answer: 1

    >>> print(user_response)
    1

    >>> user_response = ask_question('What's 9 + 10?', '19', '21', 'Both', '')
    'What's 9 + 10?'
    1 19
    2 21
    3 Both
    Your answer: 1

    >>> print(user_response)
    1
    """

    option1 = str(option1)
    option2 = str(option2)
    option3 = str(option3)
    option4 = str(option4)

    print(question)

    if option1 != "": #lists available answer options
        print("1", option1) 
    
    if option2 != "":
        print("2", option2)

    if option3 != "":
        print("3", option3)

    if option4 != "":
        print("4", option4)
    
    answer = str(input("Your Answer: ")) #prompts user to answer question

    if answer == '1' or answer == '2' or answer == '3' or answer == '4':
        return answer

    else: #user answers with invalid option
        print("Error: Invalid Answer")
        answer = "Error"
        return answer

def km_to_miles(km):
    """ (float) -> float, 2
    Returns km in miles rounded to 2 decimals

    >>> km_to_miles(0)
    0

    >>> km_to_miles(3.5)
    2.17

    >>> km_to_miles(-1)
    "Error: Negative Number"
    """

    if km >= 0: #only prints if equal to 0 or positive
        miles = km / KILOMETRES_PER_MILE #conversion from km to miles
        miles = float(round(miles, 2)) #rounds miles to 2 decimal places

    else:
        print("Error: Negative Number of km") #negative km input
        miles = 0
    
    return miles

def minutes_to_hour_string(minutes):
    """ (float) -> str
    Returns minutes simplified to hours and minutes

    >>> minutes_to_hour_string(199)
    3 hours and 19.0 minutes

    >>> minutes_to_hour_stirng(60)
    1 hour

    >>> minutes_to_hour_string(-60)
    "Error: Negative Number"
    """

    minutes = float(minutes)

    if minutes <= 0: #if minutes input were negative
        time_string = "Error: Negative Number"

    elif minutes < MINUTES_PER_HOUR: #less than an hour
        minutes = str(minutes)
        time_string = minutes + " minutes"
        
    elif minutes == MINUTES_PER_HOUR: #exactly 1 hour
        time_string = "1 hour"
       
    elif minutes%60 == 0: #an exact amount of hours with no remaining minutes
        hours = int(minutes/MINUTES_PER_HOUR)
        hours = str(hours)
        time_string = hours + " hours"
        
    elif minutes > MINUTES_PER_HOUR and minutes%60 != 0: #more than 1 hour with minutes remaining
        minutes_hold = minutes #separate variable from minutes to hold original value
        minutes = round(float(minutes%MINUTES_PER_HOUR), 2)
        minutes_hold = float(minutes_hold - minutes) #subtracts remainder minutes from original; multiple of 60
        hours = int(minutes_hold / MINUTES_PER_HOUR)

        minutes = str(minutes)
        hours = str(hours)

        if minutes == "1.0" and hours == "1": #specific case for single hour and single minute
            time_string = (hours + " hour and " + minutes + " minute")

        elif minutes == "1": #specific case for single mintues
            time_string = (hours + " hours and " + minutes + " minute")
            
        elif hours == "1": #specific case for single hour
            time_string = (hours + " hour and " + minutes + " minutes")

        else: #multiple hours and mulitple minutes
            time_string = (hours + " hours and " + minutes + " minutes")


    return time_string

def display_welcome():
    """ (NoneType) -> NoneType
    Prints welcome message

    >>> display_welcome()
    ------------------------------------------
    -- Welcome to the Road Trip Calculator! --
    ------------------------------------------
    """

    print("-" * 42)
    
    print("-- Welcome to the Road Trip Calculator! --")

    print("-" * 42)


def fuel_consumption(distance_in_miles):
    """ (float) -> float
    Returns the amount of fuel consumed after traveling distance_in_miles
    
    >>> fuel_consumption(30.0)
    1.0

    >>> fuel_consumption(-60.0)
    2.0

    >>> fuel_consumption(0.0)
    0.0
    """

    distance_in_miles = abs(distance_in_miles) #if negative input, absolute value is taken since the magnitude of distance is being calculated
    distance_in_miles = float(distance_in_miles)
   
    gallons = (distance_in_miles/MILES_PER_GALLON)
    
    return gallons

def get_trip_fuel(distance_from_start_to_end, initial_fuel):
    """ (float, float) -> float
    Returns amount of extra fuel needed to travel distance_from_start_to_end with initial_fuel 
    
    >>> get_trip_fuel(600.0, 15.0)
    5.0

    >>> get_trip_fuel(-600, 15.0) #should still work with negative distance
    5.0
    
    >>> get_trip_fuel(-600, -15.0)
    "Error: Negative Initial Fuel"

    >>> get_trip_fuel(31, 1)
    0.033333

    >>> get_trip_fuel(30, 1)
    0.0
    """

    distance_from_start_to_end = abs(distance_from_start_to_end) #only magnitude of distance matters for fuel consumption
    distance_from_start_to_end = float(distance_from_start_to_end)

    total_fuel_required = distance_from_start_to_end/MILES_PER_GALLON

    if initial_fuel >= 0:
        if total_fuel_required > initial_fuel: #extra fuel required
            fuel_required = total_fuel_required - initial_fuel

        elif total_fuel_required <= initial_fuel: #no extra fuel required
            fuel_required = 0.0
    else: #accounts for negative input for initial_fuel
        fuel_required = "Error: Negative Initial Fuel"

    return fuel_required

def get_trip_time_with_refill(required_gallons, num_gallons_refilled_per_minute, distance_from_start_to_end):
    """ (float, float, float) -> float
    Returns the amount of time needed to complete the trip, including the amount of time it takes to refuel

    >>> get_trip_time_with_refill(1000.0, 1.0, 100.0)
    1100.0

    >>> get_trip_time_with_refill(-1.0, 0.01, 1.0)
    "Error: Negative Required Gallons and/or Negative Refill Rate"

    >>> get_trip_time_with_refill(1.0, 0.01, -1.0) #should still work with negative distance
    101.0
    """

    distance_from_start_to_end = abs(distance_from_start_to_end) # only magnitude of distance matters for fuel consumption
    distance_from_start_to_end = float(distance_from_start_to_end)

    if required_gallons < 0 or num_gallons_refilled_per_minute <= 0:  #executes if these variables are negative
        print("Error: Negative Required Gallons and/or Negative Refill Rate")

    else:
        driving_time = ((distance_from_start_to_end / MILES_PER_HOUR) * MINUTES_PER_HOUR)
        refill_time = (required_gallons / num_gallons_refilled_per_minute)

        total_time = round(float(driving_time + refill_time), 2) #sum of driving time and time to refill rounded

        return total_time

def is_trip_with_refills_possible(initial_fuel, max_fuel, trip_cost, budget, distance_to_station1, distance_to_station2, distance_from_start_to_end):
    """(float, float, float, float, float, float, float) -> bool
    Retruns a boolean depending on the possibility of the trip given the parameters regarding distance, budget, and fuel
    
    >>> is_trip_with_refills_possible(5.0, 50.0, 1000.0, 100.0, 1.0, 2.0, 3.0)
    False

    >>> is_trip_with_refills_possible(1.0, -1000.0, 1.0, 1.0, 1.0, 2.0, 3.0) #False with negative fuel value
    False

    >>> is_trip_with_refills_possible(1.0, 1000.0, 1.0, 1.0, -1.0, -2.0, -3.0) #True with negative distance inputs
    True
    """

    possible = True 

    distance_from_start_to_end = abs(distance_from_start_to_end)
    distance_to_station1 = abs(distance_to_station1)
    distance_to_station2 = abs(distance_to_station2)
    
    if initial_fuel < 0 or max_fuel < 0 or trip_cost < 0 or budget < 0: #trip can't be possible with these values as negative
        possible = False

    elif budget < trip_cost or initial_fuel * MILES_PER_GALLON < distance_to_station1\
    or get_trip_fuel(distance_from_start_to_end - distance_to_station1, max_fuel) != 0\
    or get_trip_fuel(distance_from_start_to_end - distance_to_station2, max_fuel) != 0: #can't reach destination from station 1 or 2 
        possible = False

    else:
        possible = True

    return possible 


def get_cheapest_trip_cost(initial_fuel, max_fuel, required_gallons, distance_from_start_to_end, cost_per_gallon1, cost_per_gallon2, distance_to_station1, distance_to_station2):
    """ (float, float, float, float, float, float, float, float) -> float
    Returns the cheapest total cost of the trip depending on fuel consumption


    >>> get_cheapest_trip_cost(2.0, 20.0, 1.0, 90.0, 0.0, 1.0, 30.0, 60.0)
    0.0

    >>> get_cheapest_trip_cost(0.5, 20.0, 1.0, 90.0, 2.0, 1.0, 30.0, 60.0)
    Impossible Trip; can't reach first station.
    -1

    >>> get_cheapest_trip_cost(1.0, 2.0, 1.0, 200.0, 2.0, 1.0, 30.0, 160.0)
    Impossible Trip; can't reach destination from second station.
    -1

    >>>get_cheapest_trip_cost(1.0, 10.0, 9.0, 10.0, 1.0, 4.0, 1.0, 9.0)
    0.0
    
    >>>get_cheapest_trip_cost(10.0,15.0,5.0,450.0,4.5,2.0,225,337.5)
    13.12
    
    >>>get_cheapest_trip_cost(10.0,15.0,15.0,750.0,2.0,4.5,225,337.5)
    36.25


    """

    if get_trip_fuel(distance_from_start_to_end, initial_fuel) == 0: #enough fuel to reach the end w/o filling up
        cost = 0.0

    elif get_trip_fuel(distance_to_station1, initial_fuel) != 0: #Impossible if not enough fuel to reach the first station
        print("Impossible Trip; can't reach first station.")
        cost = -1

    elif get_trip_fuel(distance_to_station2 - distance_to_station1, max_fuel) != 0: #Impossible if not enough fuel to reach the second station from first
        print("Impossible Trip; can't reach second station from first.")
        cost = -1
        
    elif get_trip_fuel(distance_from_start_to_end - distance_to_station2, max_fuel) != 0: #Impossible if can't reach end from second station
        print("Impossible Trip; can't reach destination from second station.")
        cost = -1

    elif get_trip_fuel(distance_from_start_to_end, initial_fuel) != 0 and initial_fuel * MILES_PER_GALLON >= distance_to_station2: #enough fuel to reach the second station

        if get_trip_fuel((distance_from_start_to_end - distance_to_station1), max_fuel) == 0 and \
        cost_per_gallon1 < cost_per_gallon2: #enough fuel to refill at station 1 and reach the end w/ station 1 being cheaper
            cost = float(cost_per_gallon1 * (fuel_consumption(distance_from_start_to_end - distance_to_station1) - (initial_fuel - fuel_consumption(distance_to_station1))))

        elif get_trip_fuel((distance_from_start_to_end - distance_to_station2), max_fuel) == 0 and \
        cost_per_gallon2 < cost_per_gallon1: #enough fuel to refill at station 2 and reach the end w/ station 2 being cheaper.
            cost = float(cost_per_gallon2 * (fuel_consumption(distance_from_start_to_end - distance_to_station2) - (initial_fuel - fuel_consumption(distance_to_station2))))


    elif get_trip_fuel(distance_from_start_to_end, initial_fuel) != 0 and initial_fuel * MILES_PER_GALLON >= distance_to_station1: #only enough fuel to reach the first staion

        if cost_per_gallon1 < cost_per_gallon2 and \
        get_trip_fuel((distance_from_start_to_end - distance_to_station1), max_fuel) == 0: #enough fuel to refill at station 1 and reach the end w/ station 1 being cheaper
            cost = float(cost_per_gallon1 * (fuel_consumption(distance_from_start_to_end - distance_to_station1)- (initial_fuel - fuel_consumption(distance_to_station1))))

        elif cost_per_gallon1 < cost_per_gallon2 and \
        get_trip_fuel((distance_from_start_to_end - distance_to_station1), max_fuel) != 0: #enough fuel to refill at station 1 but can't reach the end
            cost1 = float(cost_per_gallon1 * (max_fuel - (initial_fuel - fuel_consumption(distance_to_station1))))
            required_gallons = required_gallons - (max_fuel - (initial_fuel - fuel_consumption(distance_to_station1))) 
            cost2 = float(cost_per_gallon2 * (required_gallons))
            cost = cost1 + cost2

        elif cost_per_gallon2 < cost_per_gallon1 or \
        fuel_consumption(distance_to_station2 - distance_to_station1) == max_fuel: #if the second station is cheaper but MUST refill at the first station
            cost = float(cost_per_gallon1 * (fuel_consumption(distance_to_station2 - distance_to_station1) - (initial_fuel - fuel_consumption(distance_to_station1))) +\
            cost_per_gallon2 * fuel_consumption(distance_from_start_to_end - distance_to_station2))
    
    return round(cost, 2)
    


def main():
    """(noneType) -> noneType
    Greets user to calculator, collects user input for trip,\
    and returns trip possibility

    >>> main()
    ------------------------------------------
    -- Welcome to the Road Trip Calculator! --
    ------------------------------------------
    What type of vehicle will you use? car
    What color will it be?
    1 red
    2 white
    3 black
    4 other
    Your Answer: 3
    What type of fuel will your car use? gas 
    How far are you traveling (in km)? 100
    Initial Fuel Level: 2
    Max Fuel Level: 4
    Budget: $100
    Cost of fuel at station 1: $4
    Cost of fuel at station 2: $2
    Distance to station 1 (in km): 20
    Distance to station 2 (in km): 30
    Number of Gallons Refilled per Minute: 2
    The Trip is possible. /
    It will take 1 hour and 2.18 minutes and will cost $0.14.


    >>> main()
    ------------------------------------------
    -- Welcome to the Road Trip Calculator! --
    ------------------------------------------
    What type of vehicle will you use? car
    What color will it be?
    1 red
    2 white
    3 black
    4 other
    Your Answer: 2
    What type of fuel will your car use? electric
    How far are you traveling (in km)? 10000
    Initial Fuel Level: 2
    Max Fuel Level: 10
    Budget: $1
    Cost of fuel at station 1: $5
    Cost of fuel at station 2: $4
    Distance to station 1 (in km): 20
    Distance to station 2 (in km): 30
    Number of Gallons Refilled per Minute: 1
    Impossible Trip; can't reach destination from second station.
    The trip is not possible.


    >>> main()
    ------------------------------------------
    -- Welcome to the Road Trip Calculator! --
    ------------------------------------------
    What type of vehicle will you use? car
    What color will it be?
    1 red
    2 white
    3 black
    4 other
    Your Answer: 3
    What type of fuel will your car use? gas
    How far are you traveling (in km)? 100
    Initial Fuel Level: 2
    Max Fuel Level: 5
    Budget: $0
    Cost of fuel at station 1: $2
    Cost of fuel at station 2: $3
    Distance to station 1 (in km): 20
    Distance to station 2 (in km): 30
    Number of Gallons Refilled per Minute: 2
    Budget is too low for the trip.
    The trip is not possible.
    """

    display_welcome()

    vehicle = input("What type of vehicle will you use? ")

    ask_question("What color will it be?", "red", "white", "black", "other")

    fuel_type = input("What type of fuel will your " + vehicle + " use? ")

    distance_from_start_to_end = km_to_miles(float(input("How far are you traveling (in km)? ")))

    initial_fuel = float(input("Initial Fuel Level: "))

    max_fuel = float(input("Max Fuel Level: "))

    budget = float(input("Budget: $"))

    cost_per_gallon1 = float(input("Cost of fuel at station 1: $"))

    cost_per_gallon2 = float(input("Cost of fuel at station 2: $"))

    distance_to_station1 = km_to_miles(float(input("Distance to station 1 (in km): ")))

    distance_to_station2 = km_to_miles(float(input("Distance to station 2 (in km): ")))

    num_gallons_refilled_per_minute = float(input("Number of Gallons Refilled per Minute: "))


    required_gallons = get_trip_fuel(distance_from_start_to_end, initial_fuel)
    time = minutes_to_hour_string(get_trip_time_with_refill(required_gallons, num_gallons_refilled_per_minute, distance_from_start_to_end))
    trip_cost = \
    get_cheapest_trip_cost(initial_fuel, max_fuel, required_gallons, distance_from_start_to_end, cost_per_gallon1, cost_per_gallon2, distance_to_station1, distance_to_station2)
    possible = is_trip_with_refills_possible(initial_fuel, max_fuel, trip_cost, budget, distance_to_station1, distance_to_station2, distance_from_start_to_end)
    
    if trip_cost > budget:
        print("Budget is too low for the trip")

    if possible:
        print("The Trip is possible. It will take " + str(time) + " and will cost $" + str(trip_cost) + ".")

    else:
        print("The trip is not possible.")

print(minutes_to_hour_string(61))
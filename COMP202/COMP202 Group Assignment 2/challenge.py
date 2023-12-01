import random

def validate_eye(eye_string):
    '''
    str -> bool
    Returns True if the () eye is in the eye_string
    
    >>>validate_eye (||||||||||()||||||||||)
    True
    
    >>>validate_eye(||||||||||)
    False
    
    >>>validate_eye(|()|)
    True
    '''
    for char in eye_string:
        return '()' in eye_string
    
def choose_move_direction(maze_width, maze_height, x, y, temperature, exits):
    '''
    (int, int, int, int, str, list) -> str
    Returns appropriate string to direct in the maze until end of maze
    
    >>>choose_move_direction(5, 5, 0, 0, 'You feel the grounds getting colder', ['east', 'south'])
    
    '''
    dir_obj = open('latest_direction.txt', 'r') #reads contents of file containing the last direction moved
    last_direction = dir_obj.read() #assigns the last direction made to a variable
    dir_obj.close
    
    if x == 0 and y == 0: #start of maze
        direction = exits[random.randint(0, len(exits)-1)]
        while direction == 'south': #moving south = chasm
            direction = exits[random.randint(0, len(exits)-1)]

    elif len(exits) == 1:
        direction = exits[0] 

    else:
        if temperature == 'You feel the ground getting colder.': #moving away from the correct direction; need to move back to the right path
            if last_direction == 'south':
                direction = 'north'
            elif last_direction == 'north':
                direction = 'south'
            elif last_direction == 'east':
                direction = 'west'
            elif last_direction == 'west':
                direction = 'east'
        else:
            direction = exits[random.randint(0, len(exits)-1)]
            
            while True: #chooses a direction that doesn't "undo" the move recently made
                if direction == 'north' and last_direction == 'south':
                    direction = exits[random.randint(0, len(exits)-1)]
                elif direction == 'south' and last_direction == 'north':
                    direction = exits[random.randint(0, len(exits)-1)]
                elif direction == 'east' and last_direction == 'west':
                    direction = exits[random.randint(0, len(exits)-1)]
                elif direction == 'west' and last_direction == 'east':
                    direction = exits[random.randint(0, len(exits)-1)]
                else:
                    break
    
    if direction == 'north':
        y += 1
    elif direction == 'south':
        y -= 1
    elif direction == 'west':
        x -= 1
    elif direction == 'east':
        x += 1
        
    fout = open('latest_direction.txt', 'w') #records the direction moved
    fout.write(direction)
    fout.close()
        
    return direction

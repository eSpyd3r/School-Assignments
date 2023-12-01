#author: Ethan Lim 261029610
import random

def get_key(dictionary, f_obj):
    """(dict, function) -> str
    Returns key in dictionary that maps to the value yielded by f_obj
    """
    try:
        values =[]
        for key in dictionary:
            values.append(dictionary[key])
    
        if f_obj == pow:
            key_value = f_obj(values[0], values[1]) #specific for pow function
        else:
            key_value = f_obj(values) #'mapped' value

        return value_check(dictionary, key_value)

    except IndexError:
        print("No key in the dictionary maps to the desired value.")

    except TypeError:
        print("The function object has an appropriated function, but that function is incompatible with this set of values.")

    except:
        print("An unknown error has occurred")

def avg(x):
    return sum(x) / len(x)

def opp_max(x):
    return (max(x) * -1)

def value_check(dictionary, value):
    """(dict, int) -> str
    Returns key(s) from x with desired value

    """
    key_list = []

    for key in dictionary:
        if key not in key_list and dictionary[key] == value: #equates key to value
            key_list.append(key)

    return random.choice(key_list) #chooses from list

#animals = {'tiger' : 5, 'bat' : 3, 'cow' : 3, 'bear' : 4} #-> min, max, avg
#animals = {'tiger' : 4, 'bat' : 1, 'cow' : 0, 'bear' : 0}  #-> sum, works
#animals = {'tiger' : 4, 'bat' : 1} #-> pow
animals = {'tiger' : 4, 'bat' : -4} #-> opp_max

try:
    print(get_key(animals, opp_max)) #Ex 1: sum Ex 2: pow Ex 3 :  
except NameError:
    print("There is no function appropriated with the provided function object.")



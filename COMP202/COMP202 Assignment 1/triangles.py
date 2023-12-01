# Author: Ethan Lim, Alison Folger, Bianca Pozzebon, Pierre Caye, Spencer Chan
# Group 9c

import math

def is_triangle(a, b, c): # checks if a triangle can be formed w a, b, and c
	if a > 0 and b > 0 and c > 0:	# conditions for input variables
		a_and_b = a + b # conditions for triangle
		a_and_c = a + c
		b_and_c = b + c

		if a_and_b > c and a_and_b > b and b_and_c > a: #triangle inequality
			print("Yes, there is a triangle with side lengths a, b and c!")
		else:
			print("No, there isn't a triangle with side lengths a, b and c!")
	else: print("No, there isn't a triangle with side lengths a, b and c!") 


def is_special_triangle(a, b, c):
	if a == b == c: # conditions for equilateral triangle
		print("The triangle is equilateral.")

	elif a == b or b == c or c == a: # conditions for isoceles triangle if not equ. tri.
		print("The triangle is isosceles.")

	if c == math.sqrt(a ** 2 + b ** 2): # checks if variable 'c' follows pythag. th.
		print("The triangle is right-angle. ")

	if b == math.sqrt(a ** 2 + c ** 2): # checks if variable 'b'' follows pythag. th.
		print("The triangle is right-angle. ")

	if a == math.sqrt(b ** 2 + c ** 2): # checks if variable 'a' follows pythag. th.
		print("The triangle is right-angle. ")


def perimeter_of_triangle(a, b, c):
	print(a + b + c)

	
def area_of_triangle(a, b, c):
	p = a + b + c # calculates perimeter
	t = p/2 # halves 'p' and sets variable 't' in Heron's formula
	area = math.sqrt(t * (t-a) * (t-b) * (t-c)) # Heron's formula
	print(area)


def angles_of_triangle(a, b, c):
	theta_a = math.acos((b ** 2 + c ** 2 - a ** 2)/(2 * b * c)) # calculates angle A radians
	theta_b = math.acos((a ** 2 + c ** 2 - b ** 2)/(2 * a * c)) # calculates angle B radians
	theta_c = math.acos((a ** 2 + b ** 2 - c ** 2)/(2 * a * b)) # calculates angle C radians

	print(theta_a * 180/math.pi)
	print(theta_c * 180/math.pi)
	print(theta_b * 180/math.pi)


def circumscribed_circle(a, b, c):
	theta_a = math.acos((b ** 2 + c ** 2 - a ** 2)/(2 * b * c)) # calculates angle A
	r = (a/math.sin(theta_a))/2 # calculates radius using angle A from above line
	print(r)


def inscribed_circle(a, b, c):
	p = a + b + c # calculates perimeter
	t = p/2 # halves 'p' and sets variable 't' 
	theta_a = math.acos((b ** 2 + c ** 2 - a ** 2)/(2 * b * c)) # calculates angle A
	r = (t - a) * math.tan(theta_a/2) # calculates radius using angle A and 't' from above
	print(r)

def approximate_pi(n):
	theta = (2 * math.pi)/n # evaluates angle for given polygon in radians
	h = math.cos(theta/2) # sets hight related to the angle
	half_a = math.sin(theta/2) # sets length of side related to the angle
	area_of_pentagon = n * half_a * h # pi approximation for polygon w/ n sides
	print(area_of_pentagon)

#author: Ethan Lim 261029610

import turtle
"""(noneType) -> noneType
Draws picture consisteng of an aquamarine hexagon, 6 red circles,/
2 orange half circles, an aquamarine triangle, and an orange 'E.'
"""

def my_artwork():
    t = turtle.Turtle()
    
    t.hideturtle() #hides cursor
    t.speed("fastest") #increases speed of drawing
    
    t.fillcolor("aquamarine2") #color of hexagon
    t.begin_fill()
    
    for i in range(6): #draws hexagon
        t.forward(200)
        t.left(360/6)
    
    t.end_fill()

    r = 25 #sets radii of circles
    for i in range(6): #draws circles
        t.forward(200)
        t.penup()
        t.forward(25)
        t.pendown()
        t.fillcolor("red") #colors the circles red
        t.begin_fill()
        t.circle(25) #draws circle
        t.end_fill()
        t.penup()
        t.backward(25)
        t.left(360 / 6)
        t.pendown()
    
    t.penup() #lifts pen to move to desired location w/o lines
    t.left(90)
    t.forward(300)
    t.right(90)
    t.forward(100)
    t.fillcolor("orange") #colors top half circle orange
    t.begin_fill()
    t.pendown()
    t.circle(20, 180) #top half circle in pattern
    t.end_fill()
    
    t.fillcolor("orange") #colors bottom half circle orange
    t.begin_fill()
    t.left(90)
    t.forward(40)
    t.right(90)
    t.circle(20, 180) #bottom half circle in pattern
    t.left(90)
    t.forward(40)
    t.end_fill()
    
    t.penup()
    t.goto(70, 220) #moves to location on screen instead of maneuvering
    t.right(180)
    t.pendown()
    
    t.color("orange")
    t.pensize(3)
    
    for i in range(3): #draws first initial of name
        t.left(90)
        t.forward(60)
        t.backward(60)
        t.right(90)
        t.forward(45)
    
    t.color("black") #outline of triangle
    t.fillcolor("aquamarine4") #color of triangle
    t.begin_fill()
    t.left(60)
    t.forward(50)
    t.right(120)
    t.forward(50)
    t.right(120)
    t.forward(50)
    t.end_fill()

my_artwork()
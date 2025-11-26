'''
    CS5001 Fall 2025
    Kartik Kulkarni
    Classes for project
'''
from turtle import Turtle
class Card:
    '''
        Class Card
        Attributes: turtle, flipped, matched, value, x, y
        Methods: flip, dissappear, match, move, change_design
    '''

    def __init__(self, flipped_status = False, matched_status = False, value = '', turtle = '', x = 0, y = 0):
        self.flipped = flipped_status
        self.matched = matched_status
        self.turtle = turtle
        self.value = value
        self.x = x
        self.y = y

    def flip(self):
        if self.flipped == False:
            self.turtle.shape(self.value)
            self.flipped = True
        else:
            self.turtle.shape('card_back.gif')
            self.flipped = False
            
    def disappear(self):
        self.turtle.hideturtle()

    def appear(self):
        self.turtle.showturtle()
        
    def change_design(self, new_value):
        self.value = new_value
        if self.flipped == True:
            self.turtle.shape(new_value)
            
    def match(self):
        self.matched = True
        self.turtle.hideturtle()
        
    def move(self, newx, newy):
        self.turtle.penup()
        self.turtle.goto(newx, newy)
        self.x = newx
        self.y = newy
        
class Button:
    '''
    Class Button
    Attributes: turtle, value, x, y
    Methods: 
    '''

    def __init__(self, value, x, y):
        self.turtle = Turtle()
        self.value = value
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.shape(value)
        self.x = x
        self.y = y
        
class Border:
    '''
    Class Border
    Attributes: turtle, width, height
    Methods: draw
    '''

    def __init__(self, turtle, width, height):
        self.turtle = turtle
        self.width = width
        self.height = height

    def draw(self, color, thickness, x, y):
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.pendown()
        self.turtle.color(color)
        self.turtle.pensize(thickness)
        for i in range(2):
            self.turtle.forward(self.width)
            self.turtle.right(90)
            self.turtle.forward(self.height)
            self.turtle.right(90)
        self.turtle.hideturtle()

import turtle
import math

ob = turtle.Turtle()
ob.speed(100)
ob.color('blue', "cyan")
ob.begin_fill()
for i in range(450):
    ob.forward(3)
    ob.left(math.sin(45))
ob.end_fill()


turtle.done()
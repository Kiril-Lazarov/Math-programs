import turtle
import random

jeff = turtle.Turtle()
jeff.color("cyan", "yellow")
jeff.pensize(10)
jeff.shape("arrow")
jeff.begin_fill()
jeff.circle(100)
jeff.end_fill()

tim = turtle.Turtle()
tim.penup()
tim.goto(-200, -200)
tim.pendown()
tim.shape("turtle")
tim.color("red", "black")
tim.begin_fill()
tim.circle(100)
tim.end_fill()
tim.penup()
tim.goto(200,-200)
tim.pendown()
tim.begin_fill()
tim.circle(100)
tim.end_fill()
tim.color("blue", "white")
for i in range(6):
    rand1 = random.randrange(-300, 300)
    rand2 = random.randrange(-300, 300)
    tim.penup()
    tim.setpos((rand1, rand2))
    tim.pendown()
    tim.begin_fill()
    tim.circle(random.randrange(10, 100))
    tim.end_fill()



turtle.done()
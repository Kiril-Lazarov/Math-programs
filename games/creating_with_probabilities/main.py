import time
import turtle
import random
from math import floor

# items = list(range(1,10)) * 2 + list(range(11,20))
#
# result = random.choices(items, k = 10000)
# print(len([x for x in result if x < 11]))

wn = turtle.Screen()
wn.title('Probabilities')
wn.bgcolor('Green')
wn.setup(width=800, height=700)
wn.tracer(0)

# obj = turtle.Turtle()
# obj.shape('circle')
# obj.shapesize(stretch_wid=0.1)
# obj.goto(0,0)
# obj.penup()

class DotFactory(turtle.Turtle):

    @classmethod
    def create_dot(cls):
        obj = turtle.Turtle()
        obj.shape('circle')
        obj.shapesize(stretch_wid=0.3)
        obj.penup()
        return obj



a = DotFactory()
dot_list = [a.create_dot() for _ in range(100)]


while True:
    wn.update()
    for dot in dot_list:
        x = random.randint(-50,51)
        y = random.randint(-50,51)
        dot.goto(x, y)
        # time.sleep(0.1)


import turtle

bob = turtle.Turtle()
bob.color("red", "blue")
bob.begin_fill()
for i in range(8):
    bob.right(45)
    bob.forward(100)
bob.left(180)
bob.forward(100)
for i in range(8):
    bob.right(45)
    bob.forward(100)
bob.end_fill()

turtle.done()
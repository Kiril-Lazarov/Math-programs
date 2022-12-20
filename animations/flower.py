import turtle

flower = turtle.Turtle()
flower.speed(8)
flower.color("red", "yellow")
flower.begin_fill()
for i in range(36):
    flower.forward(350)
    flower.right(170)
flower.end_fill()



turtle.done()
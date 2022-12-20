import turtle
import time

wn = turtle.Screen()
wn.title("moving circle")
wn.bgcolor("cyan")

wn.register_shape(r"C:\Потребители\lenovo\Documents\Paint 3D frames/blue line.gif")
wn.register_shape(r"C:\Потребители\lenovo\Documents\Paint 3D frames/blue line2.gif")
line = turtle.Turtle()
line.shape(r"C:\Потребители\lenovo\Documents\Paint 3D frames/blue line.gif")
def line_animate():
    if line.shape() == "C:\Потребители\lenovo\Documents\Paint 3D frames/blue line.gif":
        line.shape(r"C:\Потребители\lenovo\Documents\Paint 3D frames/blue line2.gif")
    elif line.shape() == "C:\Потребители\lenovo\Documents\Paint 3D frames/blue line2.gif":
        line.shape(r"C:\Потребители\lenovo\Documents\Paint 3D frames/blue line.gif")
    wn.ontimer(line_animate, 500)

turtle.done()

# C:\Users\lenovo\Documents\Paint 3D frames
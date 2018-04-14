import turtle
import random
p = turtle.Pen()
def drawleft(size):
    p.left(90)
    color=[random.randint(0.0, 1.0),random.randint(0.0, 1.0),random.randint(0.0, 1.0)]
    p.begin_fill()
    p.fillcolor(color)
    for x in range(3):
        p.forward(size)
        p.left(120)
    p.end_fill()
def drawSqure(size):
    color=[random.randint(0.0, 1.0),random.randint(0.0, 1.0),random.randint(0.0, 1.0)]
    p.begin_fill()
    p.fillcolor(color)
    for x in range(4):
        p.forward(size)
        p.left(90)
    p.end_fill()
def drawright(size):
    p.left(30)
    color=[random.randint(0.0, 1.0),random.randint(0.0, 1.0),random.randint(0.0, 1.0)]
    p.begin_fill()
    p.fillcolor(color)
    for x in range(3):
        p.forward(size)
        p.left(120)
    p.end_fill()
    drawleft(100)
    p.right(90)
    drawSqure(100)
    p.forward(100)
    drawright(100)
    turtle.done()
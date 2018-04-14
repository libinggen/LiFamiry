import turtle
p = turtle.Pen()
p.penup()
p.goto(-100,0)
p.pendown()

p.left(180)
p.forward(100)
p.right(90)
p.forward(200)
p.right(153.5)
p.forward(223.6)
p.left(63.5)
for x in range (3):
    p.forward(250)
    p.left(120)


p.forward(250)

p.forward(100)
p.left(90)
p.forward(200)
p.left(153.5)
p.forward(223.6)


turtle.done()
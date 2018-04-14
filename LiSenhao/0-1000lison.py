import turtle
import random
p = turtle .Pen ()
for x in range (1000):
    p.penup()
    p.setpos(random.randint(-300, 300),random.randint(-300, 300))
    p.pendown()
    number = random.randint(0, 1000)
    p.write(number,font=('Arial'))

turtle.done()
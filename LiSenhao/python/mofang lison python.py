import turtle
p = turtle.Pen()
p.pencolor('red')
p.goto(200,0)
p.goto(200,200)
p.goto(0,200)
p.goto(0,0)
p.pencolor('orange')
p.penup()
p.goto(100,100)
p.pendown()
p.goto(-100,100)
p.goto(-100,-100)
p.goto(100,-100)
p.goto(100,100)
p.pencolor('yellow')
p.goto(200,200)
p.penup()
p.goto(-100,100)
p.pendown()
p.goto(0,200)
p.goto(0,0)

p.goto(-100,-100)
p.goto(100,-100)
p.goto(200,0)
turtle.done()
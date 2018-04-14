import turtle      #导入turtle库
h=turtle .Pen ()    #创建一个画笔变量h
colors=["red",'blue','orange'] 
for  x in range (111):
    h.pencolor(colors[x%3])
    h .forward(200)
    h.left(92)
h.penup()
h.setpos(60,100)
h.pendown()
h.write("Lison's Coding",font= (50))
h.hideturtle()
#h.reset()
turtle .done ()
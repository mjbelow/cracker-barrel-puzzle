import tkinter, math


def update():
    lbl.configure(text=str(p1.get())+", "+str(p2.get())+", "+str(p3.get())+", "+str(p4.get())+", "+str(p5.get())+", "+str(p6.get())+", "+str(p7.get())+", "+str(p8.get())+", "+str(p9.get())+", "+str(p10.get())+", "+str(p11.get())+", "+str(p12.get())+", "+str(p13.get())+", "+str(p14.get())+", "+str(p15.get()))

window = tkinter.Tk()
window.geometry("550x550")
window.title("Cracker Barrel Puzzle")


p1=tkinter.IntVar(value=1)
p2=tkinter.IntVar(value=1)
p3=tkinter.IntVar(value=1)
p4=tkinter.IntVar(value=1)
p5=tkinter.IntVar(value=1)
p6=tkinter.IntVar(value=1)
p7=tkinter.IntVar(value=1)
p8=tkinter.IntVar(value=1)
p9=tkinter.IntVar(value=1)
p10=tkinter.IntVar(value=1)
p11=tkinter.IntVar(value=1)
p12=tkinter.IntVar(value=1)
p13=tkinter.IntVar(value=1)
p14=tkinter.IntVar(value=1)
p15=tkinter.IntVar(value=1)

top=50
vert_dist=horz_dist=100

tkinter.Checkbutton(window, relief="sunken", variable=p1, command=update).place(relx=0.5, rely=0, x=-25, y=top, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p2, command=update).place(relx=0.5, rely=0, x=-25-horz_dist/2, y=top+vert_dist, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p3, command=update).place(relx=0.5, rely=0, x=-25+horz_dist/2, y=top+vert_dist, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p4, command=update).place(relx=0.5, rely=0, x=-25-horz_dist, y=top+vert_dist*2, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p5, command=update).place(relx=0.5, rely=0, x=-25, y=top+vert_dist*2, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p6, command=update).place(relx=0.5, rely=0, x=-25+horz_dist, y=top+vert_dist*2, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p7, command=update).place(relx=0.5, rely=0, x=-25-horz_dist/2-horz_dist, y=top+vert_dist*3, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p8, command=update).place(relx=0.5, rely=0, x=-25-horz_dist/2, y=top+vert_dist*3, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p9, command=update).place(relx=0.5, rely=0, x=-25+horz_dist/2, y=top+vert_dist*3, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p10, command=update).place(relx=0.5, rely=0, x=-25+horz_dist/2+horz_dist, y=top+vert_dist*3, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p11, command=update).place(relx=0.5, rely=0, x=-25-horz_dist*2, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p12, command=update).place(relx=0.5, rely=0, x=-25-horz_dist, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p13, command=update).place(relx=0.5, rely=0, x=-25, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p14, command=update).place(relx=0.5, rely=0, x=-25+horz_dist, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p15, command=update).place(relx=0.5, rely=0, x=-25+horz_dist*2, y=top+vert_dist*4, height=50, width=50)

lbl = tkinter.Label(window,text=str(p1.get())+", "+str(p2.get())+", "+str(p3.get())+", "+str(p4.get())+", "+str(p5.get())+", "+str(p6.get())+", "+str(p7.get())+", "+str(p8.get())+", "+str(p9.get())+", "+str(p10.get())+", "+str(p11.get())+", "+str(p12.get())+", "+str(p13.get())+", "+str(p14.get())+", "+str(p15.get()))
lbl.pack()

# canvas = tkinter.Canvas()
# canvas.create_line(100, 600, 600, 600, 350, 600-math.sqrt(3)*250, 100, 600)
# canvas.pack(fill=tkinter.BOTH, expand=1)

# canvas = tkinter.Canvas()
# canvas.create_line(0, 0, 500, 500, 500, 250)
# canvas.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

window.mainloop()
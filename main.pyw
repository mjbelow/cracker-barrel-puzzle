import tkinter, math


def update():
    lbl.configure(text=str(p[0].get())+", "+str(p[1].get())+", "+str(p[2].get())+", "+str(p[3].get())+", "+str(p[4].get())+", "+str(p[5].get())+", "+str(p[6].get())+", "+str(p[7].get())+", "+str(p[8].get())+", "+str(p[9].get())+", "+str(p[10].get())+", "+str(p[11].get())+", "+str(p[12].get())+", "+str(p[13].get())+", "+str(p[14].get()))

# valid_moves={
# 1:[[2,4],[3,6]],
# 2:[[5,9],[4,7]],
# 3:[[5,8],[6,10]],
# 4:[[]],
# 5:[[]],
# 6:[[]],
# 7:[[]],
# 8:[[]],
# 9:[[]],
# 10:[[]],
# 11:[[]],
# 12:[[]],
# 13:[[]],
# 14:[[]],
# 15:[[]],
# }

window = tkinter.Tk()
window.geometry("550x550")
window.title("Cracker Barrel Puzzle")


p=[0]*15;

for i in range(0,15):
    p[i]=tkinter.IntVar(value=1)

top=50
vert_dist=horz_dist=100

tkinter.Checkbutton(window, relief="sunken", variable=p[0], command=update).place(relx=0.5, rely=0, x=-25, y=top, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p[1], command=update).place(relx=0.5, rely=0, x=-25-horz_dist/2, y=top+vert_dist, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[2], command=update).place(relx=0.5, rely=0, x=-25+horz_dist/2, y=top+vert_dist, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p[3], command=update).place(relx=0.5, rely=0, x=-25-horz_dist, y=top+vert_dist*2, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[4], command=update).place(relx=0.5, rely=0, x=-25, y=top+vert_dist*2, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[5], command=update).place(relx=0.5, rely=0, x=-25+horz_dist, y=top+vert_dist*2, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p[6], command=update).place(relx=0.5, rely=0, x=-25-horz_dist/2-horz_dist, y=top+vert_dist*3, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[7], command=update).place(relx=0.5, rely=0, x=-25-horz_dist/2, y=top+vert_dist*3, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[8], command=update).place(relx=0.5, rely=0, x=-25+horz_dist/2, y=top+vert_dist*3, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[9], command=update).place(relx=0.5, rely=0, x=-25+horz_dist/2+horz_dist, y=top+vert_dist*3, height=50, width=50)


tkinter.Checkbutton(window, relief="sunken", variable=p[10], command=update).place(relx=0.5, rely=0, x=-25-horz_dist*2, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[11], command=update).place(relx=0.5, rely=0, x=-25-horz_dist, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[12], command=update).place(relx=0.5, rely=0, x=-25, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[13], command=update).place(relx=0.5, rely=0, x=-25+horz_dist, y=top+vert_dist*4, height=50, width=50)
tkinter.Checkbutton(window, relief="sunken", variable=p[14], command=update).place(relx=0.5, rely=0, x=-25+horz_dist*2, y=top+vert_dist*4, height=50, width=50)

lbl = tkinter.Label(window,text=str(p[0].get())+", "+str(p[1].get())+", "+str(p[2].get())+", "+str(p[3].get())+", "+str(p[4].get())+", "+str(p[5].get())+", "+str(p[6].get())+", "+str(p[7].get())+", "+str(p[8].get())+", "+str(p[9].get())+", "+str(p[10].get())+", "+str(p[11].get())+", "+str(p[12].get())+", "+str(p[13].get())+", "+str(p[14].get()))
lbl.pack()

# canvas = tkinter.Canvas()
# canvas.create_line(100, 600, 600, 600, 350, 600-math.sqrt(3)*250, 100, 600)
# canvas.pack(fill=tkinter.BOTH, expand=1)

# canvas = tkinter.Canvas()
# canvas.create_line(0, 0, 500, 500, 500, 250)
# canvas.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

window.mainloop()
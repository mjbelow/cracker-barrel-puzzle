import tkinter, math, copy, os

clear = lambda: os.system("cls")

def configure(event):
    # center=window.winfo_width()//2
    center=event.width//2
    canvas.delete("all")
    tri_1 = center, top+25
    tri_2 = center+tri_height/math.sqrt(3), top+25+tri_height
    tri_3 = center-tri_height/math.sqrt(3), top+25+tri_height
    canvas.create_polygon(tri_1, tri_2 , tri_3, width=2, fill="SystemButtonFace", outline="#000")    

def update():
    for i in range(total):
        piece_values[i]=piece[i].get()

finished=False

def start():
    global found, finished
    found=False
    finished=False
    move(True, copy.copy(piece_values), [])


def move(first, pieces, move_history):
    global found, finished
    moved=False

    # if there are less pegs than you want for a solution, stop going down that path
    count=0
    for i in range(total):
        if(pieces[i]==1):
            count+=1
    peg_count_option=False
    if(peg_operator.get()=="<" or peg_operator.get()=="<="):
        peg_count_option=False
    elif(peg_operator.get()=="=" or peg_operator.get()==">="):
        peg_count_option=count < peg_count.get()
    else:
        peg_count_option=count <= peg_count.get()
    if(peg_count_option):
        return

    for i in range(total):
        if(found_limit.get() and found >= found_limit_value.get()):
            if not finished:
                finished=True
                print("---------------------")
            return
        if(pieces[i]==1):
            for j in range(len(valid_moves[i])):
                piece_jump=pieces[valid_moves[i][j][0]]
                piece_dest=pieces[valid_moves[i][j][1]]
                if(piece_jump==1 and piece_dest==0):
                    moved=True
                    pieces_adjust=copy.copy(pieces)

                    # make the move
                    pieces_adjust[i]=0
                    pieces_adjust[valid_moves[i][j][0]]=0
                    pieces_adjust[valid_moves[i][j][1]]=1

                    # record the move
                    my_move=[i]
                    my_move.append(valid_moves[i][j])
                    my_move_history=copy.copy(move_history)
                    my_move_history.append(my_move)

                    # find more available moves
                    move(False,pieces_adjust,my_move_history)
    if(not moved):
        count=0
        for i in range(total):
            if(pieces[i]==1):
                count+=1
        # print(move_history)
        # print("remaining pieces",count)
        peg_count_option=False
        if(peg_operator.get()=="<"):
            peg_count_option=count < peg_count.get()
        elif(peg_operator.get()=="<="):
            peg_count_option=count <= peg_count.get()
        elif(peg_operator.get()=="="):
            peg_count_option=count == peg_count.get()
        elif(peg_operator.get()==">="):
            peg_count_option=count >= peg_count.get()
        else:
            peg_count_option=count > peg_count.get()
        if(peg_count_option):
            found+=1
            print()
            print(move_history)
            print("remaining pieces: ",count)
            print("solution count: ",found)
            print()
        move_history=[]
    if(first):
        print("---------------------")

def clear_all():
    for i in range(total):
        piece[i].set(0)
    update()

def mark_all():
    for i in range(total):
        piece[i].set(1)
    update()

valid_moves=[
    # 0
    [[1,3],[2,5]],
    # 1
    [[3,6],[4,8]],
    # 2
    [[4,7],[5,9]],
    # 3
    [[1,0],[4,5],[7,12],[6,10]],
    # 4
    [[7,11],[8,13]],
    # 5
    [[4,3],[8,12],[2,0],[9,14]],
    # 6
    [[3,1],[7,8],[10,15],[11,17]],
    # 7
    [[4,2],[8,9],[11,16],[12,18]],
    # 8
    [[7,6],[4,1],[12,17],[13,19]],
    # 9
    [[5,2],[8,7],[13,18],[14,20]],
    # 10
    [[6,3],[11,12]],
    # 11
    [[7,4],[12,13]],
    # 12
    [[11,10],[7,3],[8,5],[13,14]],
    # 13
    [[12,11],[8,4]],
    # 14
    [[13,12],[9,5]],
    # 15
    [[10,6],[16,17]],
    # 16
    [[11,7],[17,18]],
    # 17
    [[16,15],[11,6],[12,8],[18,19]],
    # 18
    [[17,16],[12,7],[13,9],[19,20]],
    # 19
    [[18,17],[13,8]],
    # 20
    [[19,18],[14,9]]
]

window = tkinter.Tk()
window.geometry("550x600")
window.title("Cracker Barrel Puzzle")

found=0
peg_count=tkinter.IntVar(value=1)
peg_count_choices=set()
found_limit=tkinter.BooleanVar(value=True)
found_limit_value=tkinter.IntVar(value=1)
peg_operator=tkinter.StringVar(value="=")

rows = 6
total = rows * (rows + 1) // 2
piece=[0]*total
piece_values=[0]*total
puzzle=[0]*total

for i in range(total):
    piece[i]=tkinter.IntVar(value=1)
    piece_values[i]=1
    peg_count_choices.add(i+1)
    puzzle[i]=tkinter.Checkbutton(window)

top=100
horz_dist=100
vert_dist=horz_dist/2*math.sqrt(3)
tri_height=(rows-1)*vert_dist

canvas = tkinter.Canvas()
canvas.bind("<Configure>", configure)
canvas.configure(background="SystemButtonFace")
canvas.place(x=0,y=0,  relwidth=1, relheight=1)

# generate puzzle board
for i in range(total):
    puzzle[i].configure(indicatoron=False, variable=piece[i], command=update, text=i, selectcolor="#ccc")
for i in range(rows):
    for j in range(i+1):
        n=j+(i*(i+1)//2)
        c = i // 2
        pos2 = -1
        offset = 0
        if i % 2 == 1:
            if j > c:
                c+=1
                pos2 = 1
            offset = horz_dist/2*pos2
        pos = j-c
        puzzle[n].place(relx=0.5,rely=0,x=-25+offset+horz_dist*pos,y=top+vert_dist*i,height=50, width=50)
        puzzle[n].lift(canvas)

tkinter.Button(window, command=clear_all, text="Clear All").place(relx=0.5,y=0,x=-255, width=80)
tkinter.Button(window, command=mark_all, text="Mark All").place(relx=0.5,y=30,x=-255, width=80)
tkinter.OptionMenu(window, found_limit_value, 1,2,3,4,5,10,20,30,40,50,100,200,300,400,500,1000,2000,3000,4000,5000).place(relx=0.5,y=25,x=-170, width=80)
tkinter.Checkbutton(window, variable=found_limit, text="Found Limit").place(relx=0.5,y=0,x=-170, width=100)
tkinter.Button(window, command=start, text="Solve").place(relx=0.5,y=0,x=-45, width=80)
tkinter.Button(window, command=clear, text="Clear").place(relx=0.5,y=30,x=-45, width=80)
tkinter.OptionMenu(window, peg_count, *peg_count_choices).place(relx=0.5,y=25,x=90, width=80)
tkinter.Label(window, text="Peg Count").place(relx=0.5,y=0,x=90, width=80)
tkinter.OptionMenu(window, peg_operator, "<","<=","=",">=",">").place(relx=0.5,y=0,x=175, width=80)

window.mainloop()
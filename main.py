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

window = tkinter.Tk()
window.geometry("550x600")
window.title("Cracker Barrel Puzzle")

found=0
peg_count=tkinter.IntVar(value=1)
peg_count_choices=set()
found_limit=tkinter.BooleanVar(value=True)
found_limit_value=tkinter.IntVar(value=1)
peg_operator=tkinter.StringVar(value="=")

rows = 5
total = rows * (rows + 1) // 2
piece=[0]*total
piece_values=[0]*total
puzzle=[0]*total
puzzle_position=[]
valid_moves=[0]*total

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

# place each piece and figure out valid moves for the piece
for i in range(rows):
    # min and max pieces of this row
    MIN = i * (i + 1) // 2
    MAX = MIN + i
    # up values based on min and max pieces of the row 2 rows ABOVE this one
    UP_MIN = (i-2) * ((i-2) + 1) // 2
    UP_MAX = UP_MIN + (i-2)
    # down values based on min and max pieces of the row 2 rows BELOW this one
    DOWN_MIN = (i+2) * ((i+2) + 1) // 2
    DOWN_MAX = DOWN_MIN + (i+2)
    for j in range(i+1):
        # piece number
        n=j+(i*(i+1)//2)

        # piece movements
        BL=[n+(i+1), n+(i+1)*2+1]
        BR=[n+(i+1)+1, n+((i+1)+1)*2+1]
        UR=[n-i, n-(i*2-1)]
        UL=[n-(i+1), n-((i+1)*2-1)]
        R=[n+1, n+2]
        L=[n-1, n-2]

        valid_moves[n]=[]

        if i < rows-2:
            # bottom left movement
            if BL[1] >= DOWN_MIN and BL[1] <= DOWN_MAX:
                valid_moves[n].append([BL[0], BL[1]])

            # bottom right movement
            if BR[1] >= DOWN_MIN and BR[1] <= DOWN_MAX:
                valid_moves[n].append([BR[0], BR[1]])

        if i >= 2:
            # up right movement
            if UR[1] >= UP_MIN and UR[1] <= UP_MAX:
                valid_moves[n].append([UR[0], UR[1]])

            # up left movement
            if UL[1] >= UP_MIN and UL[1] <= UP_MAX:
                valid_moves[n].append([UL[0], UL[1]])

            # left movement
            if L[1] >= MIN:
                valid_moves[n].append([L[0], L[1]])
            # right movement
            if R[1] <= MAX:
                valid_moves[n].append([R[0], R[1]])

        c = i // 2
        pos2 = -1
        offset = 0
        if i % 2 == 1:
            if j > c:
                c+=1
                pos2 = 1
            offset = horz_dist/2*pos2
        pos = j-c
        puzzle_position.append([-25+offset+horz_dist*pos, top+vert_dist*i])
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
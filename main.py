import tkinter, math, copy, os, functools

clear = lambda: os.system("cls")

def draw_board_lines():
    center=window.winfo_width()//2
    canvas.delete("all")
    # draw lines connecting all pieces
    for i in range(rows):
        # min and max pieces of this row
        MIN = i * (i + 1) // 2
        MAX = MIN + i
        # min and max pieces of final row
        LAST_MIN = (rows-1) * rows // 2
        LAST_MAX = LAST_MIN + (rows-1)
        # position of min and max piece for this row
        MIN_POS = center + puzzle_position[MIN][0], puzzle_position[MIN][1]
        MAX_POS = center + puzzle_position[MAX][0], puzzle_position[MAX][1]
        # position of min piece for final row (increasing by 1 each time)
        LAST_MIN_POS = center + puzzle_position[LAST_MIN+i][0], puzzle_position[LAST_MIN+i][1]
        # position of max piece for final row (decreasing by 1 each time)
        LAST_MAX_POS = center + puzzle_position[LAST_MAX-i][0], puzzle_position[LAST_MAX-i][1]
        # horizontal lines
        canvas.create_line(MIN_POS, MAX_POS, width=1, fill="#000")
        # top-left to bottom-right lines
        canvas.create_line(MIN_POS, LAST_MAX_POS, width=1, fill="#000")
        # top-right to bottom-left lines
        canvas.create_line(MAX_POS, LAST_MIN_POS, width=1, fill="#000")

def configure(event):
    draw_board_lines()

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
        if(first):
            print("---------------------")
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

rows = 5
total = rows * (rows + 1) // 2
piece=[0]*total
piece_values=[0]*total
puzzle=[0]*total
puzzle_position=[]
valid_moves=[0]*total

top=100
horz_dist=100
vert_dist=horz_dist/2*math.sqrt(3)
piece_size=50
piece_size_half=piece_size//2
tri_width=(rows)*horz_dist
tri_height=(rows-1)*vert_dist

window = tkinter.Tk()
window.geometry(str(tri_width+piece_size)+"x"+str(math.ceil(tri_height+piece_size*2)+top))
window.title("Cracker Barrel Puzzle")

found=0
peg_count=tkinter.IntVar(value=1)
peg_count_choices=set()
found_limit=tkinter.BooleanVar(value=True)
found_limit_value=tkinter.IntVar(value=1)
peg_operator=tkinter.StringVar(value="=")

class puzzle_piece(tkinter.Checkbutton):
    def __init__(self, master, number):
        super().__init__(master)
        self.number = number
        self.bind("<Enter>", functools.partial(self.show_moves, False))
        self.bind("<ButtonRelease-1>", functools.partial(self.show_moves, True))
        self.bind("<Leave>", self.clear_moves)

    def show_moves(self, release, event):
        draw_board_lines()
        center=window.winfo_width()//2

        piece_src=self.number
        active=piece[piece_src].get()
        if release:
            active = not active
        # draw lines to valid moves
        for move in valid_moves[piece_src]:
            piece_jump=move[0]
            piece_dest=move[1]
            if active and piece[piece_jump].get() and (not piece[piece_dest].get()):
                line_start=center+puzzle_position[piece_src][0], puzzle_position[piece_src][1]
                line_end=center+puzzle_position[piece_dest][0], puzzle_position[piece_dest][1]
                # draw line from this piece to valid move locations
                canvas.create_line(line_start, line_end, width=3, fill="#f00")

    def clear_moves(self, event):
        draw_board_lines()

for i in range(total):
    piece[i]=tkinter.IntVar(value=1)
    piece_values[i]=1
    peg_count_choices.add(i+1)
    puzzle[i]=puzzle_piece(window,i)

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
        puzzle_position.append([-piece_size_half+offset+horz_dist*pos + piece_size_half, top+vert_dist*i + piece_size_half])
        puzzle[n].place(relx=0.5,rely=0,x=-piece_size_half+offset+horz_dist*pos,y=top+vert_dist*i,height=piece_size, width=piece_size)
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
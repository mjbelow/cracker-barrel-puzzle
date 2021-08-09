#!/usr/bin/env python

try:
    import tkinter
    from tkinter import ttk
except:
    import Tkinter as tkinter
    import ttk
import math, copy, os, functools, platform

window = tkinter.Tk()
window.title("Cracker Barrel Puzzle")

# function to clear terminal dependent on system
if(platform.system() == "Windows"):
    clear = lambda: os.system("cls")
else:
    clear = lambda: os.system("clear")

# theme of app
lightGray="#d9d9d9"
darkGray="#aaa"
validMovesColor="#f00"

#offset of buttons from top
yTopOffset=5

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

def separator():
    print("---------------------")

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
        # if this is the first move, there won't be any more solutions found, so print a separator to indicate it's done solving
        if(first):
            separator()
        return

    for i in range(total):
        if(found_limit.get() and found >= found_limit_value.get()):
            if not finished:
                finished=True
                # separate each solution group
                separator()
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
    # no more valid moves could be made; see if this series of moves is a solution according to the set [peg count] compared to this solution's peg count using the set [logical operator]
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
            print("")
            print(move_history)
            print("remaining pieces: %d" % count)
            print("solution count: %d" % found)
            print("")
            # to separate each individual solution, uncomment this and comment out [separate each solution group]
            # separator()
        move_history=[]
    if(first and not finished):
        separator()

def clear_all():
    for i in range(total):
        piece[i].set(0)
    update()

def mark_all():
    for i in range(total):
        piece[i].set(1)
    update()

def update_rows(name, index, operation):
    init(rows_value.get(), False)
    draw_board_lines()

class puzzle_piece(tkinter.Checkbutton, object):
    def __init__(self, master, number):
        super(self.__class__, self).__init__(master)
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
                canvas.create_line(line_start, line_end, width=3, fill=validMovesColor)

    def clear_moves(self, event):
        draw_board_lines()

class puzzle_button(ttk.Button, object):
    def __init__(self, master, **kwargs):
        kwargs["takefocus"]=False
        super(self.__class__, self).__init__(master, **kwargs)

rows_value = tkinter.IntVar(value=5)
rows_value.trace("w",update_rows)

canvas = tkinter.Canvas(highlightthickness=0)
canvas.bind("<Configure>", configure)
canvas.configure(background=lightGray)
canvas.place(x=0,y=0,  relwidth=1, relheight=1)

def init(rows_count, first):
    global rows, total, piece, piece_values, puzzle, puzzle_position, valid_moves, top, horz_dist, vert_dist, piece_size, piece_size_half, tri_width, tri_height, found, peg_count, peg_count_choices, found_limit, found_limit_value, peg_operator, peg_count_options

    if not first:
        for i in range(total):
            puzzle[i].place_forget()

    rows = rows_count
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

    if tri_width+piece_size < 550:
        window.geometry("550x"+str(int(math.ceil(tri_height+piece_size*2)+top)))
    else:
        window.geometry(str(tri_width+piece_size)+"x"+str(int(math.ceil(tri_height+piece_size*2)+top)))

    found=0
    peg_count_choices=set()
    if first:
        peg_count=tkinter.IntVar(value=1)
        found_limit=tkinter.BooleanVar(value=True)
        found_limit_value=tkinter.IntVar(value=1)
        peg_operator=tkinter.StringVar(value="=")

    peg_count_choices.add(0)
    for i in range(total):
        piece[i]=tkinter.IntVar(value=1)
        piece_values[i]=1
        peg_count_choices.add(i+1)
        puzzle[i]=puzzle_piece(window,i)

    # generate puzzle board
    for i in range(total):
        puzzle[i].configure(indicatoron=False, variable=piece[i], command=update, text=i, selectcolor=darkGray, background=lightGray)

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

    if first:
        s = ttk.Style()
        s.configure("TMenubutton", background=lightGray)
        s.configure("TCheckbutton", background=lightGray)
        clear_all_btn = puzzle_button(window, command=clear_all, text="Clear All")
        clear_all_btn.place(relx=0.5,y=yTopOffset+0,x=-255, width=80)
        mark_all_btn = puzzle_button(window, command=mark_all, text="Mark All")
        mark_all_btn.place(relx=0.5,y=yTopOffset+30,x=-255, width=80)
        row_options=ttk.OptionMenu(window, rows_value, 0,1,2,3,4,5,6,7,8,9,10,11,12)
        row_options.place(relx=0.5,y=yTopOffset+60,x=-255, width=80)
        limit_options=ttk.OptionMenu(window, found_limit_value, 0,1,2,3,4,5,10,20,30,40,50,100,200,300,400,500,1000,2000,3000,4000,5000)
        limit_checkbox=ttk.Checkbutton(window, variable=found_limit, text="Found Limit")
        limit_options.place(relx=0.5,y=yTopOffset+25,x=-170, width=80)
        limit_checkbox.place(relx=0.5,y=yTopOffset+0,x=-170, width=100)
        solve=puzzle_button(window, command=start, text="Solve")
        solve.place(relx=0.5,y=yTopOffset+0,x=-45, width=80)
        clear_console=puzzle_button(window, command=clear, text="Clear")
        clear_console.place(relx=0.5,y=yTopOffset+30,x=-45, width=80)
        peg_count_options=ttk.OptionMenu(window, peg_count, *peg_count_choices)
        peg_count_options.place(relx=0.5,y=yTopOffset+25,x=175, width=80)
        peg_count_label=tkinter.Label(window, text="Peg Count", bg=lightGray)
        peg_count_label.place(relx=0.5,y=yTopOffset+0,x=90, width=80)
        operator=ttk.OptionMenu(window, peg_operator, "","<","<=","=",">=",">")
        operator.place(relx=0.5,y=yTopOffset+25,x=90, width=80)
    else:
        peg_count_options.set_menu(*peg_count_choices)

init(5, True)
window.mainloop()

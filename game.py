#!/bin/python3
from tkinter import *
from random import randint
from PIL import ImageTk, Image
from ScrollableFrame import ScrollableFrame
from WidgetsPro import ButtonPro
from turns import AVALIBLE_TURNS
from ScrollableCanvas import ScrollableCanvas, ButtonSC

def get_dst(line, column):
    res = 2e9
    for l1, c1 in CELLS:
        res = min(res, abs(line - l1) + abs(column - c1))
    return res

class BgFg:
    def __init__(self, bg="#fff", fg="#000"):
        self.bg = bg
        self.fg = fg
    
    def draw(self, w):
        w['bg'] = self.bg
        w['fg'] = self.fg
        w['activebackground'] = self.bg
        w['activeforeground'] = self.fg

def cheat(ev=None):
    if len(cheats) > 0:
        while len(cheats) > 0:
            cheats[-1].destroy()
            cheats.pop()
            if MODE == 1:
                grid_info = cheats[-1].grid_info()
                btns[grid_info['row']][grid_info['column']].grid(row=grid_info['row'], column=grid_info['column'])
    else:
        for i, j, in CELLS:
            if MODE == 0:
                cheats.append(Button(field, font=FONT, bg="#f00", activebackground="#f00", activeforeground="#000", text="X", command=cheat))
                cheats[-1].place(relx=BTN_WIDTH * j + BTN_PAD * j + BTN_WIDTH / 4, rely=BTN_HEIGHT * i + BTN_PAD * i + BTN_HEIGHT / 4,
                            relwidth=BTN_WIDTH / 2, relheight=BTN_HEIGHT / 2)
            elif MODE == 1:
                cheats.append(ButtonPro(field, fixwidth=50, fixheight=50, font=FONT, bg="#f00", activebackground="#f00", activeforeground="#000", text="X", command=cheat))
                btns[i][j].grid_forget()
                cheats[-1].grid(row=i, column=j)
            elif MODE == 2:
                cheats.append(ButtonSC(field, font=FONT, bg="#f00", fg="#000", command=cheat, text="X"))
                cheats[-1].place(x=50 * j + 5 * j + 12.5, y=50 * i + 5 * i + 12.5, width=25, height=25)

def choose(wid):
    if wid['text'] == "?":
        if wid['bg'] == CLOSED_COLOR.bg:
            CHOOSED_COLOR.draw(wid)
        else:
            CLOSED_COLOR.draw(wid)

def re_color(i, j, fg=True):
    dst = get_dst(i, j)
    SCHEMES[SCHEME](dst).draw(btns[i][j])
    btns[i][j]['text'] = dst
    if fg:
        btns[i][j]['fg'] = "#880"
        btns[i][j]['activeforeground'] = "#880"
        lastTurn.append((i, j))
    return dst == 0

def clearLastTurn():
    for i, j in lastTurn:
        re_color(i, j, False)

def turn(i, j):
    global REWARD

    have = False
    for i2, j2 in AVALIBLE_TURNS[CURRENT_TURN][1]:
            line = i + i2
            column = j + j2
            if 0 <= line < HEIGHT and 0 <= column < WIDTH and (btns[line][column]['bg'] == CLOSED_COLOR.bg or btns[line][column]['bg'] == CHOOSED_COLOR.bg):
                have = True
                break
    if not have:
        return
    clearLastTurn()
    if coins < AVALIBLE_TURNS[CURRENT_TURN][0]:
        wnd = Label(root, text="НЕДОСТАТОЧНО\nДЕНЕГ\nДЛЯ ХОДА", font=FONT_BOLD, bg="#fdd")
        wnd.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
        wnd.after(1000, lambda *args: wnd.destroy())
    else:
        guessed = 0
        updateCoins(-AVALIBLE_TURNS[CURRENT_TURN][0])
        for i2, j2 in AVALIBLE_TURNS[CURRENT_TURN][1]:
            line = i + i2
            column = j + j2
            if 0 <= line < HEIGHT and 0 <= column < WIDTH and (btns[line][column]['bg'] == CLOSED_COLOR.bg or btns[line][column]['bg'] == CHOOSED_COLOR.bg):
                guessed += re_color(line, column)
        if guessed == 1:
            text = f"ВЫ УГАДАЛИ КЛЕТКУ\nИ ПОЛУЧИЛИ НАГРАДУ: {REWARD} 🪙"
            updateCoins(REWARD)
            REWARD += round(REWARD / 4)
        elif guessed > 1:
            form = "ОК" if (11 < guessed % 100 < 20 or 5 <= guessed % 10 <= 9 or guessed % 10 == 0) else ("КУ" if guessed % 10 == 1 else "КИ")
            text = f"ВЫ УГАДАЛИ {guessed} КЛЕТ{form}\nИ ПОЛУЧИЛИ НАГРАДЫ: "
            su = 0
            for i in range(guessed):
                text += str(REWARD)
                su += REWARD
                updateCoins(REWARD)
                REWARD += round(REWARD / 4)
                if i != guessed - 1:
                    text += "+"
            text += f"\nВ СУММЕ: {su} 🪙"
        if guessed > 0:
            wnd = Label(root, text=text, font=FONT_BOLD, bg="#dfd")
            wnd.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
            wnd.after(2000, lambda *args: wnd.destroy())


def moveUp(i, j):
    btns[(i - 1) % HEIGHT][j].focus_set()
def moveDown(i, j):
    btns[(i + 1) % HEIGHT][j].focus_set()
def moveLeft(i, j):
    btns[i][(j - 1) % WIDTH].focus_set()
def moveRight(i, j):
    btns[i][(j + 1) % WIDTH].focus_set()

def schemeStandart(dst):
    COLORS = {
        0: BgFg("#050", "#000"),
        1: BgFg("#080", "#000"),
        2: BgFg("#0f0", "#000"),
        3: BgFg("#7f0", "#000"),
        4: BgFg("#af8", "#000"),
        5: BgFg("#cf8", "#000"),
        6: BgFg("#ff8", "#000"),
        7: BgFg("#fc8", "#000"),
        8: BgFg("#fa8", "#000"),
        9: BgFg("#fad", "#000")
    }
    return COLORS.get(dst, BgFg("#fff", "#000"))

def schemeGreen(dst):
    # from GREEN to WHITE
    # from  0f0 to fff
    if dst == 0:
        return BgFg("#393", "#fff")
    col_integer = 255 - int(255 * (0.75 ** (dst - 1)))
    chars = "0123456789abcdef"
    st = chars[col_integer // 16] + chars[col_integer % 16]
    return BgFg("#" + st + "ff" + st)

def openAll():
    clearLastTurn()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            re_color(i, j)

def updateCoins(num=0):
    global coins
    coins += num
    btnCoins['text'] = f"{coins} 🪙"

def changeTurn(turnName):
    global CURRENT_TURN
    NOT_TURN_COLOR.draw(turns[CURRENT_TURN][0])
    NOT_TURN_COLOR.draw(turns[CURRENT_TURN][1])
    CURRENT_TURN = turnName
    CUR_TURN_COLOR.draw(turns[CURRENT_TURN][0])
    CUR_TURN_COLOR.draw(turns[CURRENT_TURN][1])
    
def updateImage(turn_):
    btn = turns[turn_][0]
    btn.update()
    img = Image.open(f"imgs/turns/{turn_}.png")
    mi = min(btn.winfo_width(), btn.winfo_height())
    img = img.resize((mi, mi), Image.LANCZOS)
    images[turn_] = ImageTk.PhotoImage(img)
    btn['image'] = images[turn_]

def resizeField(ev):
    if MODE != 0:
        return
    fieldFr.update()
    w = fieldFr.winfo_width()
    h = fieldFr.winfo_height()
    szOne = min(w / WIDTH, h / HEIGHT)
    wid = szOne * WIDTH / w
    hei = szOne * HEIGHT / h
    field.place(relx=(1 - wid) / 2, rely=(1 - hei) / 2, relwidth=wid, relheight=hei)

def startDistanceCounting(ev, i, j):
    global start_place
    start_place = (i, j)
    btn_startplace.place(ev.x - 12.5, ev.y - 12.5, 25, 25)

def showDistance(ev, i, j):
    btn_distance['text'] = abs(i - start_place[0]) + abs(j - start_place[1])
    btn_distance.place(ev.x - 12.5, ev.y - 12.5, 25, 25)

def stopDistanceCounting():
    global start_place
    start_place = None
    btn_startplace.destroy(False)
    btn_distance.destroy(False)

images = {}
RED, GREEN, YELLOW, BLUE, WHITE = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[0m"
# WIDTH = int(input(f"Type a {RED}WIDTH{WHITE}:\t"))
# HEIGHT = int(input(f"Type a {RED}HEIGHT{WHITE}:\t"))
# NUMB = int(input(f"Type a {GREEN}NUMBER{WHITE} of {RED}CELLS{WHITE}:\t"))
# SCHEME = input(f"Type a {BLUE}SCHEME{WHITE}:\t").lower()
# coins = int(input(f"Type a number of {YELLOW}COINS{WHITE}:\t"))
# FONTSIZE = int(input(f"Type a suze of FONT:\t"))
# MODE = input(f"Type a mode of view screen: (F)it or (S)croll or (C)anvas scroll\t").lower()
WIDTH = 36
HEIGHT = 20
NUMB = 3
SCHEME = "g"
coins = 10
FONTSIZE = 20
MODE = "c"
if MODE == "f":
    MODE = 0
elif MODE == "s":
    MODE = 1
elif MODE == "c":
    MODE = 2
else:
    print(f"{RED}ERROR: MODE is not F/S/C")
    input()
    exit()
CLOSED_COLOR = BgFg("#333", "#fff")
CHOOSED_COLOR = BgFg("#777", "#fff")
CELLS = []
while len(CELLS) < NUMB:
    coord = (randint(0, HEIGHT - 1), randint(0, WIDTH - 1))
    if coord not in CELLS:
        CELLS.append(coord)

DEFAULT_COLOR = BgFg()
SCHEMES = {
    "standart": schemeStandart,
    "s": schemeStandart,

    "green": schemeGreen,
    "g": schemeGreen
}
cheats = []
root = Tk()
root["bg"] = "#000"
root.bind("<Control-Shift-C>", cheat)
root.bind("<Control-Shift-S>", lambda ev: openAll())

fieldFr = Frame(root)
info = Frame(root)
fieldFr.place(relx=0.0, rely=0.1, relwidth=1.0, relheight=0.9)
info.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.1)

if MODE == 0:
    field = Frame(fieldFr)
    field.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
elif MODE == 1:
    fieldAll = ScrollableFrame(fieldFr)
    field = fieldAll.content
else:
    field = ScrollableCanvas(fieldFr)

btns = []
BTN_PAD = 0.002
# x*WIDTH + btn_pad * WIDTH - btn_pad = 1
BTN_WIDTH = (1 - BTN_PAD * (WIDTH - 1)) / WIDTH
BTN_HEIGHT = (1 - BTN_PAD * (HEIGHT - 1)) / HEIGHT

FONT = ("Consolas", FONTSIZE)
FONT_BOLD = ("Consolas", FONTSIZE, "bold")

if MODE == 2:
    start_place = None
    btn_startplace = ButtonSC(field, "#ff9", "#000", FONT_BOLD)
    btn_distance = ButtonSC(field, "#9f9", "#000", FONT_BOLD)
    field.bind("<Button3-Motion>", lambda event: btn_distance.destroy(False))
    field.bind("<ButtonRelease-3>", lambda event: stopDistanceCounting())
for i in range(HEIGHT):
    btns.append([])
    for j in range(WIDTH):
        if MODE == 0:
            btns[i].append(Button(field, font=FONT, text="?"))
            btns[i][j].place(relx=BTN_WIDTH * j + BTN_PAD * j, rely=BTN_HEIGHT * i + BTN_PAD * i,
                            relwidth=BTN_WIDTH, relheight=BTN_HEIGHT)
        elif MODE == 1:
            btns[i].append(ButtonPro(field, font=FONT, text="?", fixwidth=50, fixheight=50))
            btns[i][j].grid(row=i, column=j)
        else:
            btns[i].append(ButtonSC(field, font=FONT, text="?"))
            btns[i][j].place(x=50 * j + 5 * j, y=50 * i + 5 * i, width=50, height=50)
            btns[i][j].bind("<Button3-Motion>", lambda event, _i=i, _j=j: showDistance(event, _i, _j))
            btns[i][j].bind("<ButtonPress-3>", lambda event, _i=i, _j=j: startDistanceCounting(event, _i, _j))
        CLOSED_COLOR.draw(btns[i][j])
        btns[i][j].bind("<Button-1>", lambda event, x=i, y=j: turn(x, y))
        btns[i][j].bind("<Control-Button-1>", lambda event, _i=i, _j=j: choose(btns[_i][_j]))
        btns[i][j].bind("<Button-2>", lambda event, _i=i, _j=j: choose(btns[_i][_j]))
        btns[i][j].bind("<Return>", lambda event, x=i, y=j: re_color(x, y))
        btns[i][j].bind("<Up>", lambda event, x=i, y=j: moveUp(x, y))
        btns[i][j].bind("<Down>", lambda event, x=i, y=j: moveDown(x, y))
        btns[i][j].bind("<Left>", lambda event, x=i, y=j: moveLeft(x, y))
        btns[i][j].bind("<Right>", lambda event, x=i, y=j: moveRight(x, y))

if MODE == 1:
    fieldAll.ready()
elif MODE == 2:
    field.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

btnCoins = Button(info, font=FONT)
btnCoins.place(relx=0.0, rely=0.0, relwidth=1/3, relheight=1.0)
updateCoins(0)
root.bind("<Control-Shift-A>", lambda *args: updateCoins(100))
lastTurn = []
CURRENT_TURN = "SINGLE"
CUR_TURN_COLOR = BgFg("#9f9")
NOT_TURN_COLOR = BgFg("#999")
turns = {}
for turnName, infoTurn in AVALIBLE_TURNS.items():
    btn = Button(info)
    btn.place(relx=1/3 + (2/3) / len(AVALIBLE_TURNS) * len(turns), rely=0.0, relwidth=(2/3) / len(AVALIBLE_TURNS), relheight=2/3)
    lbl = Label(info, text=f"{infoTurn[0]} 🪙", font=FONT)
    lbl.place(relx=1/3 + (2/3) / len(AVALIBLE_TURNS) * len(turns), rely=2/3, relwidth=(2/3) / len(AVALIBLE_TURNS), relheight=1/3)
    NOT_TURN_COLOR.draw(btn)
    NOT_TURN_COLOR.draw(lbl)
    turns[turnName] = (btn, lbl)
    btn.bind("<Button-1>", lambda event, _turn=turnName: changeTurn(_turn))
    # updateImage(turnName)
    btn.bind("<Configure>", lambda event, turnName_=turnName: updateImage(turnName_))
changeTurn("SINGLE")
REWARD = 5
fieldFr.bind("<Configure>", resizeField)
root.mainloop()

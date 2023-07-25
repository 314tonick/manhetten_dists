#!/bin/python3
from tkinter import *
from random import randint
from PIL import ImageTk, Image
from ScrollableFrame import ScrollableFrame
from WidgetsPro import ButtonPro
from turns import AVALIBLE_TURNS
from ScrollableCanvas import ScrollableCanvas, ButtonSC

def game(WIDTH, HEIGHT, NUMB, SCHEME, coins, MODE, REWARDS, call_back, geometry=None):
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
                    cheats.append(Button(field, font=FONT_MAIN_SMALL, bg="#f00", activebackground="#f00", activeforeground="#000", text="X", command=cheat))
                    cheats[-1].place(relx=BTN_WIDTH * j + BTN_PAD * j + BTN_WIDTH / 4, rely=BTN_HEIGHT * i + BTN_PAD * i + BTN_HEIGHT / 4,
                                relwidth=BTN_WIDTH / 2, relheight=BTN_HEIGHT / 2)
                elif MODE == 1:
                    cheats.append(ButtonPro(field, fixwidth=50, fixheight=50, font=FONT_MAIN, bg="#f00", activebackground="#f00", activeforeground="#000", text="X", command=cheat))
                    btns[i][j].grid_forget()
                    cheats[-1].grid(row=i, column=j)
                elif MODE == 2:
                    cheats.append(ButtonSC(field, font=FONT_MAIN_SMALL, bg="#f00", fg="#000", command=cheat, text="X"))
                    cheats[-1].place(x=BTN_WIDTH * j + BTN_WIDTH / 10 * j + BTN_WIDTH / 4, y=BTN_HEIGHT * i + BTN_HEIGHT / 10 * i + BTN_HEIGHT / 4, width=BTN_WIDTH / 2, height=BTN_HEIGHT / 2)

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
        nonlocal reward_index

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
            wnd = Label(root, text="НЕДОСТАТОЧНО\nДЕНЕГ\nДЛЯ ХОДА", font=FONT_BIG, bg="#fdd")
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
            rews = []
            for i in range(guessed):
                rews.append(REWARDS[reward_index])
                updateCoins(REWARDS[reward_index])
                reward_index += 1
            if guessed == 1:
                text = f"ВЫ УГАДАЛИ КЛЕТКУ\nИ ПОЛУЧИЛИ НАГРАДУ: {rews[0]} 🪙"
            elif guessed > 1:
                form = "ОК" if (11 < guessed % 100 < 20 or 5 <= guessed % 10 <= 9 or guessed % 10 == 0) else ("КУ" if guessed % 10 == 1 else "КИ")
                text = f"ВЫ УГАДАЛИ {guessed} КЛЕТ{form}\nИ ПОЛУЧИЛИ НАГРАДЫ: "
                su = 0
                for i in range(guessed):
                    text += str(rews[i])
                    su += rews[i]
                    if i != guessed - 1:
                        text += "+"
                text += f"\nВ СУММЕ: {su}🪙"
            if guessed > 0:
                wnd = Label(root, text=text, font=FONT_BIG, bg="#dfd")
                wnd.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
                wnd.after(2000, lambda *args: wnd.destroy())
                if reward_index == len(REWARDS):
                    end = Frame(root)
                    Label(end, text=f"ВЫ НАШЛИ ВСЕ КЛЕТКИ\nИ ПОЛУЧИВ {coins}🪙\nВЫ ВЫИГРАЛИ!!!", font=FONT_BIG, bg="#191").place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
                    Button(end, text="OK", font=FONT_SMALL, bg="#bbf", command=root.destroy).place(relx=0.35, rely=0.8, relwidth=0.2, relheight=0.1)
                    end.after(2000, end.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0))
            else:
                if coins == 0:
                    end = Frame(root)
                    Label(end, text="У ВАС ЗАКОНЧИЛИСЬ МОНЕТЫ\nИ ВЫ ПРОИГРАЛИ!", font=FONT_BIG, bg="#911").place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
                    Button(end, text="OK", font=FONT_SMALL, bg="#bbf", command=root.destroy).place(relx=0.35, rely=0.8, relwidth=0.2, relheight=0.1)
                    end.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

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
        nonlocal coins
        coins += num
        btnCoins['text'] = f"{coins} 🪙"

    def changeTurn(turnName):
        nonlocal CURRENT_TURN
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
        nonlocal start_place
        start_place = (i, j)
        btn_startplace.place(ev.x - BTN_WIDTH / 4, ev.y - BTN_HEIGHT / 4, BTN_WIDTH / 2, BTN_HEIGHT / 2)

    def showDistance(ev, i, j):
        if start_place is None:
            return
        btn_distance['text'] = abs(i - start_place[0]) + abs(j - start_place[1])
        btn_distance.place(ev.x - BTN_WIDTH / 4, ev.y - BTN_HEIGHT / 4, BTN_WIDTH / 2, BTN_HEIGHT / 2)

    def stopDistanceCounting():
        nonlocal start_place
        start_place = None
        btn_startplace.destroy(False)
        btn_distance.destroy(False)

    def changeScale(newWidth, newHeight):
        nonlocal BTN_WIDTH, BTN_HEIGHT
        if not 0 < newWidth < 250 or not 0 < newHeight < 250:
            return
        BTN_WIDTH = newWidth
        BTN_HEIGHT = newHeight
        FONT_MAIN = ("Consolas", BTN_HEIGHT // 10 * 3)
        FONT_MAIN_SMALL = ("Consolas", BTN_HEIGHT // 10 * 3 // 2)
        btn_startplace['font'] = FONT_MAIN_SMALL
        btn_distance['font'] = FONT_MAIN_SMALL
        for cheatButton in cheats:
            cheatButton['font'] = FONT_MAIN_SMALL
        for i in range(HEIGHT):
            for j in range(WIDTH):
                btns[i][j]['font'] = FONT_MAIN
                btns[i][j].place(x=BTN_WIDTH * j + BTN_WIDTH / 10 * j, y=BTN_HEIGHT * i + BTN_HEIGHT / 10 * i, width=BTN_WIDTH, height=BTN_HEIGHT)
        field.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    def onDestoryRoot(event):
        if event.widget == root:
            call_back(reward_index == len(REWARDS), coins)

    images = {}
    FONT_BIG = ("Consolas", 50)
    FONT_SMALL = ("Consolas", 25)
    if MODE == "f":
        FONT_MAIN = ("Consolas", int(input(f"Type a size of FIELD FONT:\t")))
        MODE = 0
    elif MODE == "s":
        FONT_MAIN = ("Consolas", 20)
        print(f"{YELLOW}Warning: (S)croll mode with old ScrollableFrame is not supported, use (C)anvas mode instead of this.{WHITE}")
        MODE = 1
    elif MODE == "c":
        FONT_MAIN = ("Consolas", 20)
        MODE = 2
    else:
        print(f"{RED}ERROR: MODE is not F/S/C")
        input()
        exit()
    FONT_MAIN_SMALL = ("Consolas", FONT_MAIN[1] // 2)

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
    root = Toplevel()
    if geometry is not None:
        root.geometry(geometry)
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
        BTN_PAD = 0.002
        # x*WIDTH + btn_pad * WIDTH - btn_pad = 1
        BTN_WIDTH = (1 - BTN_PAD * (WIDTH - 1)) / WIDTH
        BTN_HEIGHT = (1 - BTN_PAD * (HEIGHT - 1)) / HEIGHT
    elif MODE == 1:
        fieldAll = ScrollableFrame(fieldFr)
        field = fieldAll.content
    else:
        field = ScrollableCanvas(fieldFr)
        root.bind("<Control-Button-5>", lambda event: changeScale(BTN_WIDTH - 5, BTN_HEIGHT - 5))
        root.bind("<Control-Button-4>", lambda event: changeScale(BTN_WIDTH + 5, BTN_HEIGHT + 5))
        BTN_WIDTH = 50
        BTN_HEIGHT = 50

    btns = []

    if MODE == 2:
        start_place = None
        btn_startplace = ButtonSC(field, "#ff9", "#000", FONT_MAIN_SMALL)
        btn_distance = ButtonSC(field, "#9f9", "#000", FONT_MAIN_SMALL)
        field.bind("<Button3-Motion>", lambda event: btn_distance.destroy(False))
        field.bind("<ButtonRelease-3>", lambda event: stopDistanceCounting())
        field.can.bind("<Leave>", lambda event: stopDistanceCounting())
    for i in range(HEIGHT):
        btns.append([])
        for j in range(WIDTH):
            if MODE == 0:
                btns[i].append(Button(field, font=FONT_MAIN, text="?"))
                btns[i][j].place(relx=BTN_WIDTH * j + BTN_PAD * j, rely=BTN_HEIGHT * i + BTN_PAD * i,
                                relwidth=BTN_WIDTH, relheight=BTN_HEIGHT)
            elif MODE == 1:
                btns[i].append(ButtonPro(field, font=FONT_MAIN, text="?", fixwidth=50, fixheight=50))
                btns[i][j].grid(row=i, column=j)
            else:
                btns[i].append(ButtonSC(field, font=FONT_MAIN, text="?"))
                btns[i][j].place(x=BTN_WIDTH * j + BTN_WIDTH / 10 * j, y=BTN_HEIGHT * i + BTN_HEIGHT / 10 * i, width=BTN_WIDTH, height=BTN_HEIGHT)
                btns[i][j].bind("<Button3-Motion>", lambda event, _i=i, _j=j: showDistance(event, _i, _j))
                btns[i][j].bind("<ButtonPress-3>", lambda event, _i=i, _j=j: startDistanceCounting(event, _i, _j))
            CLOSED_COLOR.draw(btns[i][j])
            btns[i][j].bind("<Button-1>", lambda event, x=i, y=j: turn(x, y))
            btns[i][j].bind("<Control-Button-1>", lambda event, _i=i, _j=j: choose(btns[_i][_j]))
            btns[i][j].bind("<Button-2>", lambda event, _i=i, _j=j: choose(btns[_i][_j]))

    if MODE == 1:
        fieldAll.ready()
    elif MODE == 2:
        field.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    btnCoins = Button(info, font=FONT_BIG)
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
        lbl = Label(info, text=f"{infoTurn[0]} 🪙", font=FONT_SMALL)
        lbl.place(relx=1/3 + (2/3) / len(AVALIBLE_TURNS) * len(turns), rely=2/3, relwidth=(2/3) / len(AVALIBLE_TURNS), relheight=1/3)
        NOT_TURN_COLOR.draw(btn)
        NOT_TURN_COLOR.draw(lbl)
        turns[turnName] = (btn, lbl)
        btn.bind("<Button-1>", lambda event, _turn=turnName: changeTurn(_turn))
        # updateImage(turnName)
        btn.bind("<Configure>", lambda event, turnName_=turnName: updateImage(turnName_))
    changeTurn("SINGLE")
    reward_index = 0
    fieldFr.bind("<Configure>", resizeField)
    root.bind("<Destroy>", onDestoryRoot)
    
if __name__ == "__main__":
    RED, GREEN, YELLOW, BLUE, WHITE = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[0m"
    # WIDTH = int(input(f"Type a {RED}WIDTH{WHITE}:\t"))
    # HEIGHT = int(input(f"Type a {RED}HEIGHT{WHITE}:\t"))
    # NUMB = int(input(f"Type a {GREEN}NUMBER{WHITE} of {RED}CELLS{WHITE}:\t"))
    # SCHEME = input(f"Type a {BLUE}SCHEME{WHITE}:\t").lower()
    # coins = int(input(f"Type a number of {YELLOW}COINS{WHITE}:\t"))
    # MODE = input(f"Type a mode of view screen: (F)it or (S)croll or (C)anvas scroll\t").lower()
    WIDTH1 = 36
    HEIGHT1 = 20
    NUMB1 = 3
    SCHEME1 = "g"
    coins1 = 10
    MODE1 = "c"
    REWARDS1 = [5, 7, 4]
    ro = Tk()
    game(WIDTH1, HEIGHT1, NUMB1, SCHEME1, coins1, MODE1, REWARDS1, print)
    ro.mainloop()
    
from game import game
from typing import List
from tkinter import *

class Level:
    def __init__(self, w: int, h: int, c: int, r: List[int], name:str):
        self.width = w
        self.height = h
        self.numb = len(r)
        self.coins = c
        self.rewards = r
        self.name = name
    
    def call_back(self, result, coins):
        root.deiconify()
        print(result, coins)

    def play(self):
        def _play():
            frmWant.destroy()
            root.update()
            geometry = root.geometry()
            print("smt")
            root.withdraw()
            print(game(self.width, self.height, self.numb, "g", self.coins, "c", self.rewards, self.call_back, geometry))
        frmWant = Frame(root)
        frmWant['bg'] = '#999'
        frmWant.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
        lb = Label(frmWant, font=FONT_BIG, bg="#999", text=f"УРОВЕНЬ {self.name}\n{self.width}x{self.height} {self.coins}🪙 {self.numb} [?]")
        lb.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.8)
        ok = Button(frmWant, font=FONT_BIG, text="ДА!", bg="#3f3", command=_play)
        ok.place(relx=0.15, rely=0.8, relwidth=0.2, relheight=0.1)
        no = Button(frmWant, font=FONT_BIG, text="НЕТ", bg="#f33", command=frmWant.destroy)
        no.place(relx=0.65, rely=0.8, relwidth=0.2, relheight=0.1)


FONT_BIG = ("Consolas", 50)
root = Tk()
root['bg'] = '#444'
LEVELS = [
#   (WI, HE, N, )
    Level(15, 15, 30, [10], "#1"),
    Level(30, 30, 30, [5, 4, 8], "#2")
]
for i in range(len(LEVELS)):
    lv = LEVELS[i]
    Button(root, text=lv.name, command=lambda lvl=lv: print(lvl.play())).place(relx=(0.04 + 0.2) * (i % 4) + 0.04, rely=(0.04 + 0.2) * (i // 4), relwidth=0.2, relheight=0.2)
root.mainloop()
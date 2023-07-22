from tkinter import *
from ScrollableFrame import ScrollableFrame
from WidgetsPro import ButtonPro

root = Tk()
btn = Button()
btn.pack()
root.bind("<ButtonPress-1>", lambda ev: print("Press"))
root.bind("<ButtonRelease-1>", lambda ev: print("Release"))
btn.bind("<Button1-Motion>", lambda ev: print(ev.x, ev.y))
root.mainloop()
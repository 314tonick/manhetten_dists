from tkinter import *
from ScrollableFrame import ScrollableFrame
from WidgetsPro import ButtonPro

root = Tk()
frm = ScrollableFrame(root, headerHeight=0, rowHeaderWidth=0)
for i in range(15):
    for j in range(15):
        ButtonPro(frm.content, fixwidth=50, fixheight=50, text=f"{i} {j}").grid(row=i, column=j)
frm.ready()
root.mainloop()
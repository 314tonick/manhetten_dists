from tkinter import *
from ScrollableFrame import ScrollableFrame
from WidgetsPro import ButtonPro

type = input()
if type == "1":
    root = Tk()
    frm = ScrollableFrame(root, headerHeight=0, rowHeaderWidth=0)
    for i in range(50):
        print(f"Started {i}")
        for j in range(50):
            ButtonPro(frm.content, fixwidth=50, fixheight=50, text=f"{i} {j}").grid(row=i, column=j)
    frm.ready()
    root.mainloop()
elif type == "2":
    def scroll(event):
        mov = 0
        if event.num == 5 or event.delta == -120:
            mov = 1
        elif event.num == 4 or event.delta == 120:
            mov = -1
        else:
            return 0

        if event.state == 16: # Linux scrolling down/up
            if (mov < 0 and event.widget.yview()[0] > 0.0) or (mov > 0 and event.widget.yview()[1] < 1.0):
                event.widget.yview_scroll(mov, UNITS)
        elif event.state == 17: # Linux scrolling left.right
            if (mov < 0 and event.widget.xview()[0] > 0.0) or (mov > 0 and event.widget.xview()[1] < 1.0):
                event.widget.xview_scroll(mov, UNITS)

    root = Tk()
    can = Canvas()
    can.bind("<Button-4>", scroll)
    can.bind("<Button-5>", scroll)

    scroll_x = Scrollbar(root, orient="horizontal", command=can.xview)
    can.configure(xscrollcommand=scroll_x.set)

    scroll_y = Scrollbar(root, orient="vertical", command=can.yview)
    can.configure(yscrollcommand=scroll_y.set)


    for i in range(50):
        print(f"Started {i}")
        for j in range(50):
            can.create_rectangle(i * 50, j * 50, i * 50 + 45, j * 50 + 45)
            can.create_text(i * 50 + 20, j * 50 + 20, text=f"{i} {j}")
    can.configure(scrollregion=can.bbox("all"))
    can.place(relx=0.0, rely=0.0, relwidth=0.9, relheight=0.9)
    scroll_x.place(relx=0.0, rely=0.9, relwidth=1.0, relheight=0.1)
    scroll_y.place(relx=0.9, rely=0.0, relwidth=0.1, relheight=1.0)
    root.after(1000, lambda: can.create_rectangle(5 * 50, 5 * 50, 5 * 50 + 45, 5 * 50 + 45, fill="#a00"))
    root.mainloop()
elif type == "3":
    import tkinter as tk
    def mouse_wheel(event):
        # print(dir(event))
        print(event.state)
        global count
        if event.num == 5 or event.delta == -120:
            count -= 1
        if event.num == 4 or event.delta == 120:
            count += 1
        if count < 0:
            label['text'] = f"Вверх {-count}"
        elif count == 0:
            label['text'] = "На месте"
        else:
            label['text'] = f"Вниз {count}"

    count = 0
    root = tk.Tk()
    root.title('Поверните колесо мыши')
    root['bg'] = 'darkgreen'

    # Windows
    root.bind("<MouseWheel>", mouse_wheel)

    # Linux
    root.bind("<Button-4>", mouse_wheel)
    root.bind("<Button-5>", mouse_wheel)

    label = tk.Label(root, font=('courier', 18, 'bold'), width=10)
    label.pack(padx=40, pady=40)
    root.mainloop()
else:
    root = Tk()
    can = Canvas(root)
    
    can.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
    root.mainloop()
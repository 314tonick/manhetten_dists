from tkinter import *

class ScrollableCanvas:
    def __init__(self, master=None, **kwargs):
        self.master = master
        
        self.frm = Frame(self.master)
        
        self.can = Canvas(self.frm, **kwargs)

        self.scroll_x = Scrollbar(self.frm, orient="horizontal", command=self.can.xview)
        self.can.configure(xscrollcommand=self.scroll_x.set)
        
        self.scroll_y = Scrollbar(self.frm, orient="vertical", command=self.can.yview)
        self.can.configure(yscrollcommand=self.scroll_y.set)

        self.can.place(relx=0.0, rely=0.0, relwidth=0.99, relheight=0.99)
        self.scroll_x.place(relx=0.0, rely=0.99, relwidth=1.0, relheight=0.01)
        self.scroll_y.place(relx=0.99, rely=0.0, relwidth=0.01, relheight=1.0)

        self.last_id = 0
        
        self.binds = {}
        self.__object_by_id = {}
        self.bind("<Button-4>", self._scroll)
        self.bind("<Button-5>", self._scroll)
        self.bind("<MouseWheel>", self._scroll)

    def _scroll(self, event):
        mov = 0
        if event.num == 5 or event.delta == -120:
            mov = 1
        elif event.num == 4 or event.delta == 120:
            mov = -1
        else:
            return

        if event.state == 16: # Linux scrolling down/up
            if (mov < 0 and event.widget.yview()[0] > 0.0) or (mov > 0 and event.widget.yview()[1] < 1.0):
                event.widget.yview_scroll(mov, UNITS)
        elif event.state == 17: # Linux scrolling left/right
            if (mov < 0 and event.widget.xview()[0] > 0.0) or (mov > 0 and event.widget.xview()[1] < 1.0):
                event.widget.xview_scroll(mov, UNITS)
    
    def place(self, x=None, y=None, width=None, height=None, relx=None, rely=None, relwidth=None, relheight=None, **kwargs):
        self.frm.place(x=x, y=y, width=width, height=height, relx=relx, rely=rely, relwidth=relwidth, relheight=relheight, **kwargs)
        self.can.configure(scrollregion=self.can.bbox("all"))
    
    def grid(self, row=None, column=None, rowspan=None, columnspan=None, **kwargs):
        self.frm.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.can.configure(scrollregion=self.can.bbox("all"))

    def pack(self, **kwargs):
        self.frm.pack(**kwargs)
        self.can.configure(scrollregion=self.can.bbox("all"))
    
    def __bind_event(self, eventName, event):
        self.can.update_idletasks()
        x1, y1, x2, y2 = self.can.bbox("all")

        event.x += self.can.xview()[0] * (x2 - x1)
        event.y += self.can.yview()[0] * (y2 - y1)
        funcs = []
        for func, id, x, y, width, height in self.binds.get(eventName, []):
            if x <= event.x <= x + width and y <= event.y <= y + height:
                funcs.append((id, func))
        funcs.sort()
        for id, func in funcs:
            func(event)
    
    def bind(self, event, function):
        return self.bind_range(event, function, 0, 0, 2e18, 2e18)

    def bind_range(self, event, function, x, y, width, height):
        if event in self.binds:
            self.binds[event].add((function, self.last_id, x, y, width, height))
        else:
            self.binds[event] = {(function, self.last_id, x, y, width, height)}
            self.can.bind(event, lambda ev, eventName=event: self.__bind_event(eventName, ev))
        self.__object_by_id[self.last_id] = (event, (function, self.last_id, x, y, width, height))
        self.last_id += 1
        return self.last_id - 1

    def unbind(self, id2):
        if id2 in self.__object_by_id:
            name, obj = self.__object_by_id.pop(id2)
            self.binds[name].remove(obj)
        else:
            raise TclError("Bind with this id doesn't exists.")

class ButtonSC:
    def __init__(self, master: ScrollableCanvas, bg=None, fg=None, font=None, text=None, command=None):
        self.pos = []
        self.can = master.can
        self.canvObj = master
        self.bg = bg
        self.fg = fg
        self.font = font
        self.text = text

        self.placeInfo = None
        self.binds = []
        if command is not None:
            self.binds.append(["<Button-1>", lambda ev: command(), None])
    
    def bind(self, event, func):
        self.binds.append([event, func, None])
        if self.placeInfo is not None:
            self.binds[-1][2] = self.canvObj.bind_range(event, func, *self.placeInfo)

    def destroy(self, raiseExceptions=True):
        if not self.pos:
            if raiseExceptions:
                raise TclError("Can't hide/destroy hidden button.")
        else:
            for i in range(len(self.binds)):
                self.canvObj.unbind(self.binds[i][2])
                self.binds[i][2] = None                
            self.placeInfo = None
            for pos_num in self.pos:
                self.can.delete(pos_num)
            self.pos.clear()

    def place(self, x, y, width, height):
        if self.pos and (x, y, width, height) != self.placeInfo:
            self.destroy()
        self.placeInfo = (x, y, width, height)
        self.pos.append(self.can.create_rectangle(x, y, x + width, y + height, fill=self.bg))
        self.pos.append(self.can.create_text(x + width / 2, y + width / 2, text=self.text, font=self.font, fill=self.fg))
        for i in range(len(self.binds)):
            self.binds[i][2] = self.canvObj.bind_range(self.binds[i][0], self.binds[i][1], *self.placeInfo)

    def __getitem__(self, key):
        if key == "bg" or key == "activebackground":
            return self.bg
        if key == "fg" or key == "activeforeground":
            return self.fg
        if key == "text":
            return self.text
        if key == "font":
            return self.font
        raise TclError("Bad option " + key)
    
    def __setitem__(self, key, value):
        if key == "bg" or key == "activebackground":
            self.bg = value
        elif key == "fg" or key == "activeforeground":
            self.fg = value
        elif key == "text":
            self.text = value
        elif key == "font":
            self.font = value
        else:
            raise TclError("Bad option " + key)
        if self.pos:
            x, y, width, height = self.placeInfo
            for pos_num in self.pos:
                self.can.delete(pos_num)
            self.pos.clear()
            self.pos.append(self.can.create_rectangle(x, y, x + width, y + height, fill=self.bg))
            self.pos.append(self.can.create_text(x + width / 2, y + width / 2, text=self.text, font=self.font, fill=self.fg))


if __name__ == "__main__":
    root = Tk()
    can = ScrollableCanvas(root)
    for i in range(50):
        print(f"Started {i}")
        for j in range(50):
            btn = ButtonSC(can, "green", "blue", ("Ubuntu", 15), f"{i} {j}")
            btn.place(i * 55, j * 55, 50, 50)
            btn.bind("<Button-3>", lambda event, _i=i, _j=j: print(_i, _j))
            print("smt")
    ident = can.bind("<Button-1>", lambda event: print("Hello! Left-click?", event))
    # can.bind_range("<Button-1>", lambda event: print("Hello! Range 1"), 200, 200, 100, 100)
    # can.bind_range("<Button-1>", lambda event: print("Hello! Range 2"), 400, 400, 100, 100)
    can.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
    root.mainloop()
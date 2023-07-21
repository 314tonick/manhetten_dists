from tkinter import *

def getSize(obj: Widget):
    obj.update()
    if obj.winfo_width() < 10 or obj.winfo_height() < 10:
        for me in ["pack", "grid", "place"]:
            try:
                getattr(obj, me)()
                obj.update()
                result = (obj.winfo_width(), obj.winfo_height())
                getattr(obj, me + "_forget")()
                return result
            except:
                pass
    return obj.winfo_width(), obj.winfo_height()

class CheckbuttonPro:
    def __init__(self, master=None, onBg='#000', offBg='#fff', onText='✔', offText='✗', onFg='#fff', offFg='#000', start=False, font=None, command=None, **kwargs):
        self.btn = ButtonPro(master, font=font, text=onText if start else offText, bg=onBg if start else offBg, fg=onFg if start else offFg, command=self.click, **kwargs)
        self.state = bool(start)
        self.onBg = onBg
        self.offBg = offBg
        self.onFg = onFg
        self.offFg = offFg
        self.onText = onText
        self.offText = offText
        self.command = command
        for attr in dir(self.btn):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(self.btn, attr))
    
    def getRealWidget(self):
        return self.btn.getRealWidget()

    def click(self):
        self.state = not self.state
        if self.state:
            self.btn.configure(text=self.onText, bg=self.onBg, fg=self.onFg)
        else:
            self.btn.configure(text=self.offText, bg=self.offBg, fg=self.offFg)
        if self.command != None:
            self.command()
    
    def get(self):
        return self.state

    def set(self, value):
        if bool(value) != self.state:
            self.click()
    
    def __getitem__(self, key):
        return self.btn[key]
    
    def __setitem__(self, key, value):
        self.btn[key] = value
    
    

class EntryPro:
    def __init__(self, master=None, fixwidth=None, fixheight=None, text="", **kwargs):
        if fixwidth is not None and 'width' in kwargs:
            raise ValueError('Can\'t make an entry with width and fixwidth!')
        elif fixwidth is not None:
            if fixheight is not None:
                self.frame = Frame(master, width=fixwidth, height=fixheight)
            else:
                w, h = getSize(Entry(master, width=3, **kwargs))
                self.frame = Frame(master, width=fixwidth, height=h)
            self.entry = Entry(self.frame, cnf=kwargs)
        else:
            w, h = getSize(Entry(master, cnf=kwargs))
            self.frame = Frame(master, width=w, height=fixheight if fixheight is not None else h)
            self.entry = Entry(self.frame, cnf=kwargs)
        self.frame['borderwidth'] = kwargs.get('borderwidth', None)
        state = self.entry['state']
        self.entry['state'] = NORMAL
        self.entry.delete(0, END)
        self.entry.insert(0, text)
        self.entry['state'] = state
        self.entry.place(relx=0, rely=0, relwidth=1, relheight=1)
        for name in dir(self.frame):
            if 'tk' in name or 'bbox' in name or 'pack' in name or 'grid' in name or 'place' in name or 'winfo' in name or 'update' in name or name in []:
                setattr(self, name, getattr(self.frame, name))
        for name in dir(self.entry):
            if 'after' in name or 'bind' in name or 'focus' in name or 'select' in name or name in ['get', 'insert', 'delete', 'configure', 'tk', '_last_child_ids', '_w', '_h', 'children', 'master']:
                setattr(self, name, getattr(self.entry, name))

    def getRealWidget(self):
        return self.entry
    
    def __getitem__(self, key):
        return self.entry[key]
    
    def __setitem__(self, key, value):
        self.entry[key] = value
    
    def set_text(self, text):
        state = self.entry['state']
        self.entry['state'] = NORMAL
        self.entry.delete(0, END)
        self.entry.insert(0, text)
        self.entry['state'] = state

    def set(self, text):
        self.set_text(text)

    def get_text(self):
        return self.entry.get()

    def get(self):
        return self.get_text()

class ButtonPro:
    def __init__(self, master=None, fixwidth=None, fixheight=None, **kwargs):
        if fixwidth is not None and 'width' in kwargs:
            raise ValueError('Can\'t make a button with width and fixwidth!')
        elif fixwidth is not None:
            if fixheight is not None:
                self.frame = Frame(master, width=fixwidth, height=fixheight)
            else:
                w, h = getSize(Button(master, cnf=kwargs))
                self.frame = Frame(master, width=fixwidth, height=h)
            self.button = Button(self.frame, cnf=kwargs)
        else:
            w, h = getSize(Button(master, cnf=kwargs))
            self.frame = Frame(master, width=w, height=fixheight if fixheight is not None else h)
            self.button = Button(self.frame, cnf=kwargs)
        self.frame['borderwidth'] = kwargs.get('borderwidth', None)
        self.button.place(relx=0, rely=0, relwidth=1, relheight=1)
        for name in dir(self.frame):
            if 'tk' in name or 'bbox' in name or 'pack' in name or 'grid' in name or 'place' in name or 'winfo' in name or 'update' in name or name in []:
                setattr(self, name, getattr(self.frame, name))
        for name in dir(self.button):
            if 'after' in name or 'bind' in name or 'focus' in name or 'select' in name or name in ['get', 'insert', 'delete', 'configure', 'tk', '_last_child_ids', '_w', '_h', 'children', 'master']:
                setattr(self, name, getattr(self.button, name))

    def getRealWidget(self):
        return self.button

    def __getitem__(self, key):
        return self.button[key]
    
    def __setitem__(self, key, value):
        self.button[key] = value


if __name__ == '__main__':
    root = Tk()
    root.geometry("1500x1000")

    # Frame(root, width=1000, bg="green").pack()
    ent = EntryPro(root, text="Hello")
    ent.pack()

    root.mainloop()
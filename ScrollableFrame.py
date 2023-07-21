import tkinter as tk
import sys
from WidgetsPro import *

# I am not using something like vars(tk.Grid) because that would override too many methods.
# Methods like Grid.columnconfigure are suppossed to be executed on self, not a child.
GM_METHODS_TO_BE_CALLED_ON_CHILD = (
    'pack', 'pack_configure', 'pack_forget', 'pack_info',
    'grid', 'grid_configure', 'grid_forget', 'grid_remove', 'grid_info',
    'place', 'place_configure', 'place_forget', 'place_info',
)

class AutoScrollbar(tk.Scrollbar):
    '''
    A scrollbar that hides itself if it's not needed. 
    Only works if you use the grid geometry manager.
    '''

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
            self.showing = False
        else:
            self.grid()
            self.showing = True
        tk.Scrollbar.set(self, lo, hi)

    def pack(self, *args, **kwargs):
        raise Exception('Cannot use pack with this widget.')

    def place(self, *args, **kwargs):
        raise Exception('Cannot use place with this widget.')


class ScrollableFrameImpl(tk.Frame):

    def __init__(self, master, headerHeight=0, rowHeaderWidth=0, *args, **kwargs):
        self.heH = headerHeight
        self.rheW = rowHeaderWidth
        self._parentFrame = tk.Frame(master)
        self._parentFrame['bg'] = 'blue'
        self._parentFrame.grid_rowconfigure(1, weight=1)
        self._parentFrame.grid_columnconfigure(1, weight=1)

        # scrollbars
        hscrollbar = AutoScrollbar(self._parentFrame, orient=tk.HORIZONTAL, bg="#000")
        hscrollbar.grid(row=2, column=1, sticky=tk.EW)
        self.hscr = hscrollbar

        vscrollbar = AutoScrollbar(self._parentFrame, orient=tk.VERTICAL, bg="#000")
        vscrollbar.grid(row=1, column=2, sticky=tk.NS)
        self.vscr = vscrollbar

        # canvas & scrolling
        self._parentFrame.update_idletasks()
        master.update()
        self.canvas = tk.Canvas(self._parentFrame,
                                xscrollcommand=hscrollbar.set,
                                yscrollcommand=vscrollbar.set,
                                bg="red",  # should not be visible
                                width=master.winfo_width() - self.rheW,
                                height=master.winfo_height() - self.heH)
        self.canvas.grid(row=1, column=1, sticky=tk.NSEW)

        self.header_canvas = tk.Canvas(self._parentFrame,
                                  bg="red",
                                  height=self.heH)
        self.header_canvas.grid(row=0, column=1, sticky=tk.EW)

        self.row_header_canvas = tk.Canvas(self._parentFrame,
                                       bg="red",
                                       width=self.rheW)
        self.row_header_canvas.grid(row=1, column=0, sticky=tk.NS)
        self.row_header_canvas.update()
        print("rhc width =", self.row_header_canvas.winfo_width())

        hscrollbar.config(command=self._scroll_x)
        vscrollbar.config(command=self._scroll_y)

        # self
        tk.Frame.__init__(self, self.canvas, *args, **kwargs)
        self._selfItemID = self.canvas.create_window(0, 0, window=self, anchor=tk.NW)

        self.header_window = tk.Frame(self.header_canvas, bg="white")
        self.header_window.pack(fill=tk.BOTH, expand=1)
        self._selfItemID = self.header_canvas.create_window(0, 0, window=self.header_window, anchor=tk.NW)

        self.row_header_window = tk.Frame(self.row_header_canvas, bg="white")
        self.row_header_window.pack(fill=tk.BOTH, expand=1)
        self._selfItemID = self.row_header_canvas.create_window(0, 0, window=self.row_header_window, anchor=tk.NW)

        # bindings
        self.canvas.bind('<Enter>', self._bindMousewheel)
        self.canvas.bind('<Leave>', self._unbindMousewheel)
        self.canvas.bind('<Configure>', self._onCanvasConfigure)
        self.header_window.bind("<Configure>",
                                lambda e: self.header_canvas.configure(scrollregion=self.header_canvas.bbox("all")))
        self.row_header_window.bind("<Configure>",
                                lambda e: self.row_header_canvas.configure(scrollregion=self.row_header_canvas.bbox("all")))

        # geometry manager
        for method in GM_METHODS_TO_BE_CALLED_ON_CHILD:
            setattr(self, method, getattr(self._parentFrame, method))

    def _scroll_x(self, *args):
        # print("x", args)
        self.canvas.xview_moveto(args[1])
        self.header_canvas.xview_moveto(args[1])

    def _scroll_y(self, *args):
        # print("y", args)
        self.canvas.yview_moveto(args[1])
        self.row_header_canvas.yview_moveto(args[1])

    def _bindMousewheel(self, event):
        # Windows
        self.bind_all('<MouseWheel>', self._onMousewheel)
        # Linux
        self.bind_all('<Button-4>', self._onMousewheel)
        self.bind_all('<Button-5>', self._onMousewheel)

    def _unbindMousewheel(self, event):
        # Windows
        self.unbind_all('<MouseWheel>')
        # Linux
        self.unbind_all('<Button-4>')
        self.unbind_all('<Button-5>')

    def _onMousewheel(self, event):
        if event.delta < 0 or event.num == 5:
            dy = +1
        elif event.delta > 0 or event.num == 4:
            dy = -1
        else:
            assert False

        if (dy < 0 and self.canvas.yview()[0] > 0.0) \
                or (dy > 0 and self.canvas.yview()[1] < 1.0):
            self.canvas.yview_scroll(dy, tk.UNITS)
            self.row_header_canvas.yview_scroll(dy, tk.UNITS)

        return 'break'

    def _onCanvasConfigure(self, event):
        self._updateSize(event.width, event.height)

    def _updateSize(self, canvWidth, canvHeight):
        hasChanged = False

        requWidth = self.winfo_reqwidth()
        newWidth = max(canvWidth, requWidth)
        if newWidth != self.winfo_width():
            hasChanged = True

        requHeight = self.winfo_reqheight()
        newHeight = max(canvHeight, requHeight)
        if newHeight != self.winfo_height():
            hasChanged = True

        if hasChanged:
            self.canvas.itemconfig(self._selfItemID, width=newWidth, height=newHeight)
            self.header_canvas.itemconfig(self._selfItemID, width=newWidth, height=self.heH)
            self.row_header_canvas.itemconfig(self._selfItemID, width=self.rheW, height=newHeight)
            return True

        return False

    def _updateScrollregion(self):
        bbox = (0, 0, self.winfo_reqwidth(), self.winfo_reqheight())
        self.canvas.config(scrollregion=bbox)

    def updateScrollregion(self):
        # a function called with self.bind('<Configure>', ...) is called when resized or scrolled but *not* when widgets are added or removed (is called when real widget size changes but not when required/requested widget size changes)
        # => useless for calling this function
        # => this function must be called manually when adding or removing children

        # The content has changed.
        # Therefore I need to adapt the size of self.

        # I need to update before measuring the size.
        # It does not seem to make a difference whether I use update_idletasks() or update().
        # Therefore according to Bryan Oakley I better use update_idletasks https://stackoverflow.com/a/29159152
        self._parentFrame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        self.update_idletasks()

        # self._updateSize(100, 100)
        self._updateSize(self.canvas.winfo_width(),
                         self.canvas.winfo_height())

        # update scrollregion
        self._updateScrollregion()


class ScrollableFrameObject:
    def __init__(self, scrollable, content, header, row_header):
        self.scrollable = scrollable
        self.header = header
        self.row_header = row_header
        self.content = content

    def ready(self):
        self.scrollable.updateScrollregion()

def ScrollableFrame(master, *args, **kwargs):
    scrollableFrame = ScrollableFrameImpl(master, *args, **kwargs)

    # scrollableFrame.grid_columnconfigure(0, weight=1)
    # scrollableFrame.grid_rowconfigure(0, weight=1)

    contentFrame = tk.Frame(scrollableFrame)
    contentFrame.grid(row=1, column=0, sticky=tk.NSEW)

    header = tk.Frame(scrollableFrame.header_window, height=kwargs.get("headerHeight", None))
    header.grid(row=0, column=0, sticky=tk.EW)

    row_header = tk.Frame(scrollableFrame.row_header_window, width=kwargs.get("rowHeaderWidth", None))
    row_header.grid(row=0, column=0, sticky=tk.NS)

    return ScrollableFrameObject(scrollableFrame, contentFrame, header, row_header)


# ====================  TEST  ====================
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}')
    if sys.platform == 'win32' or sys.platform == 'win64':
        root.attributes('-fullscreen', True)  
    else:
        pass
        #root.attributes('-zoomed', True)  
    root.update()
    root.geometry(f"{root.winfo_width()}x{root.winfo_height() - 200}+0+0")
    root.resizable(False, False)
    par_frame = tk.Frame(root)
    par_frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    COL_W = 5
    FONT = ("Consolas", 35)
    FONT2 = ("Consolas", 20)

    w, h = getSize(tk.Entry(root, width=COL_W, font=FONT))
    frame = ScrollableFrame(par_frame, 
    headerHeight=h,
    rowHeaderWidth=getSize(tk.Entry(root, width=COL_W, font=FONT))[0])

    for i in range(15):
        en = EntryPro(frame.row_header, text=f"RH {i}", bg="orange", font=FONT, width=COL_W)
        en.grid(row=i, column=0, padx=(0, 10), pady=(0, 10))
        
    for i in range(15):
        en = EntryPro(frame.header, fixwidth=w, fixheight=h, text=f"CH {i}", bg="yellow", font=FONT2)
        en.grid(row=0, column=i, padx=(0, 10), pady=(0, 10))

    for i in range(15):
        for j in range(15):
            # tk.Label(frame.content, text=f"{i} {j}", bg="green").place(x=100*j, y=100*i, width=90, height=90)
            en = EntryPro(frame.content, text=f"{i} {j}", bg="green", width=COL_W, font=FONT)#
            en.grid(row=i, column=j, padx=(0, 10), pady=(0, 10))

    frame.ready()
    root.mainloop()
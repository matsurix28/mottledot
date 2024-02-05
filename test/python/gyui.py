from tkinter import ttk
import tkinter as tk
import tkinterdnd2 as dnd2
from PIL import Image, ImageTk
from tkinter import filedialog

def main():
    app = Application()
    app.start()

class Application():
    def __init__(self) -> None:
        pass

    def start(self):
        root = dnd2.Tk()
        root.geometry('1120x630')
        root.title('Color Fv/Fm')
        main = MainFrame(root)
        s = ttk.Style()
        s.theme_use('classic')
        s.configure('MyWidget.TFrame', background='red')
        dtct = DetectFrame(main)
        main.add_tab(dtct, 'Detect')
        root.mainloop()

class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        self.__create_tabs()
        
    def __create_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

    def add_tab(self, frame, title):
        self.notebook.add(frame, text=title)

class DetectFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style='MyWidget.TFrame')
        self.pack(expand=True, fill='both')
        BfAfFrame(self, 'Select leaf image')

class BfAfFrame(ttk.Frame):
    def __init__(self, master, txt):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        #self.__set(txt)
        self.__test()

    def __set(self, txt):
        lbl_frame = ttk.Frame(self, style='MyWidget.TFrame')
        lbl_frame.pack(fill='x')
        sel_btn = ttk.Button(lbl_frame, text='▼')
        sel_btn.pack(side='right')
        lbl = ttk.Label(lbl_frame, text=txt, style='MyWidget.TLabel')
        lbl.pack(fill='both', expand=True)

    def __test(self):
        r = ttk.Style()
        r.theme_use('classic')
        r.configure('MyR.TFrame', background='red')
        g = ttk.Style()
        g.theme_use('classic')
        g.configure('MyG.TFrame', background='green')
        b = ttk.Style()
        b.theme_use('classic')
        b.configure('MyB.TFrame', background='blue')
        frm1 = ttk.Frame(self, style='MyR.TFrame')
        frm1.grid(row=0, column=0, sticky=tk.W+tk.E)

if __name__ == '__main__':
    main()
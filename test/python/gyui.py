from tkinter import ttk
import tkinter as tk
import tkinterdnd2 as dnd2
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np


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
        #BfAfFrame(self, 'Select leaf image')
        #frm1 = tk.Frame(self, bg='red')
        #frm1.pack(fill='both', expand=True)
        bframe = ttk.Frame(self)
        bframe.pack(expand=True, fill='both')
        aframe = ttk.Frame(self)
        aframe.pack(fill='both', expand=True)
        mthd_lbl = ttk.Label(aframe, text='Methods', anchor='center')
        mthd_lbl.pack(fill='x')
        self.b = ImageChange(bframe)
        self._method_area(aframe)
        #a = ImageChange(aframe)
        #btn = ttk.Button(self, text='OSE!!', command=self.set_img)
        #btn.pack()

    def set_img(self):
        img = cv2.imread('test/output/daen/6.png')
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((400, 200))
        img_tk = ImageTk.PhotoImage(img_pil)
        self.b.set_img(img_tk)

    def _method_area(self, master):
        master.configure(relief='groove', borderwidth=5)
        shp_frm = ttk.Frame(master, borderwidth=5, relief='raised')
        shp_frm.propagate(0)
        shp_frm.pack(side='left', expand=True, fill='both')
        grn_frm = ttk.Frame(master, borderwidth=5, relief='raised')
        grn_frm.propagate(0)
        grn_frm.pack(side='left', fill='both', expand=True)
        shp_lbl = ttk.Label(shp_frm, text='Shape')
        shp_lbl.pack()
        grn_lbl = ttk.Label(grn_frm, text='Green')
        grn_lbl.pack()
        s = ttk.Style()
        s.configure('Illust.TLabel', background='blue')
        shp_img = ttk.Label(shp_frm, style='Illust.TLabel')
        shp_img.pack(expand=True, fill='both')
        self._shape_bar(shp_frm)

    def _shape_bar(self, master):
        down_btn = ttk.Button(master, text='▼')
        down_btn.pack(side='left')
        value = ttk.Entry(master)
        value.pack(side='left', fill='x', expand=True)
        up_btn = ttk.Button(master, text='▲')
        up_btn.pack(side='right')


class BfAfFrame(ttk.Frame):
    def __init__(self, master, txt):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        self.__set(txt)
        #self.__test()

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

class ImageChange(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=5, relief='groove')
        self.pack(fill='both', expand=True)
        self.__set()

    def __set(self):
        s = ttk.Style()
        s.configure('ttt.TLabel',background='red')
        title = ttk.Label(self, text='aeui', anchor='center')
        title.grid(row=0, column=0, columnspan=3, sticky='EW')
        lbl_frame = ttk.Frame(self)
        lbl_frame.propagate(0)
        lbl_frame.grid(row=1, column=0, sticky='NSEW')
        bimg_frame = ttk.Frame(self)
        bimg_frame.propagate(0)
        bimg_frame.grid(row=2, column=0, sticky='NSEW')
        arrow_frame = ttk.Frame(self)
        arrow_frame.propagate(0)
        arrow_frame.grid(row=2, column=1)
        aimg_frame = ttk.Frame(self)
        aimg_frame.propagate(0)
        aimg_frame.grid(row=2, column=2, sticky='NSEW')
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=5)
        #self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=5)
        sel_btn = ttk.Button(lbl_frame, text='▼')
        sel_btn.pack(side='right')
        lbl = ttk.Entry(lbl_frame)
        lbl.pack(fill='both', expand=True)
        #btnb = ttk.Button(bimg_frame, text='bimg')
        #btnb.pack(fill='both', expand=True)
        img = cv2.imread('test/output/daen/1.png')
        h,w = img.shape[:2]
        self.ratio = h/w
        self.img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img_pil = Image.fromarray(self.img_rgb)
        self.img_pil_copy = self.img_pil.copy()
        #self.img_pil = self.img_pil.resize((400,200))
        self.img_tk = ImageTk.PhotoImage(self.img_pil)
        self.bimg = tk.Label(bimg_frame, bg='red')
        self.bimg.pack(expand=True, fill='both')
        
        self.bimg.bind('<Configure>', self._resize_image)
        btna = ttk.Button(arrow_frame)
        btna.pack(fill='both', expand=True)
        btnaf = tk.Label(aimg_frame, bg='blue')
        btnaf.pack(fill='both', expand=True)
        self.bimg.configure(image=self.img_tk)
        btnaf.configure(image=self.img_tk)

    

    def set_img(self, img):
        print('osaretayo...')
        self.img = img
        self.bimg.configure(image=self.img)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        new_ratio = new_height / new_width
        if new_ratio >= self.ratio:
            new_height = new_width * self.ratio
        else:
            new_width = new_height * np.reciprocal(self.ratio)
        self.img_pil = self.img_pil_copy.resize((int(new_width), int(new_height)))
        self.img_tk = ImageTk.PhotoImage(self.img_pil)
        self.bimg.configure(image=self.img_tk)

if __name__ == '__main__':
    main()
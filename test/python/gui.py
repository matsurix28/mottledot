import tkinter as tk
from tkinter import filedialog, ttk

import cv2
import numpy as np
import tkinterdnd2 as dnd2
from PIL import Image, ImageTk


def main():
    app = Application()
    app.start()

class Application():
    def __init__(self) -> None:
        self.root = dnd2.Tk()
        self.root.geometry('1280x720')
        self.root.title('Pickcell Color')
        self.main_frm = MainFrame(self.root)

    def start(self):
        detect_frm = DetectFrame(self.root)
        self.main_frm.add_tab(detect_frm, 'Detect leaf')
        fvfm_frm = FvFmFrame(self.root)
        self.main_frm.add_tab(fvfm_frm, 'Fv/Fm value')
        arrange_frm = ArrangeFrame(self.root)
        self.main_frm.add_tab(arrange_frm, 'Arrange')
        result_frm = ResultFrame(self.root)
        self.main_frm.add_tab(result_frm, 'Result')
        self.root.mainloop()

    def test_add(self, frame, title):
        self.main_frm.add_tab(frame, title)

class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
    
    def add_tab(self, frame, title):
        self.notebook.add(frame, text=title)

class DetectFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, relief='groove', borderwidth=10)
        self.thresh = tk.StringVar()
        self.min_h = tk.StringVar()
        self.max_h = tk.StringVar()
        img_frm = self._image_frame()
        method_frm = self._method_frame()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        img_frm.propagate(0)
        method_frm.propagate(0)
        img_frm.grid(row=0, column=0, sticky='NSEW')
        method_frm.grid(row=0, column=1, sticky='NSEW')

    def _image_frame(self):
        img_frm = ttk.Frame(self)
        before_frm = ImageFrame(img_frm)
        img = Image.open('src/arrow.png')
        img = img.resize((48,48))
        self.img = ImageTk.PhotoImage(img)
        space_frm = ttk.Frame(img_frm, height=30)
        arrow = tk.Label(img_frm, image=self.img)
        after_frm = ImageFrame(img_frm, out=True)
        img_frm.grid_columnconfigure(0, weight=1)
        img_frm.grid_rowconfigure(0, weight=5)
        img_frm.grid_rowconfigure(3, weight=5)
        before_frm.grid(row=0, column=0, sticky='NSEW')
        space_frm.grid(row=1, column=0)
        arrow.grid(row=2, column=0)
        after_frm.grid(row=3, column=0, sticky='NSEW')
        before_frm.propagate(0)
        after_frm.propagate(0)
        return img_frm
    
    def _method_frame(self):
        method_frm = tk.Frame(self)
        methods = ('Detect contours', 'Extract Green area')
        select_box = ttk.Combobox(method_frm, state='readonly', values=methods, font=('Calibri', 12))
        select_box.set('Detect contours')
        select_box.bind('<<ComboboxSelected>>', self._select_method)
        cnt_frm = self._contour_method_frame(method_frm)
        grn_frm = self._green_method_frame(method_frm)
        method_frm.grid_columnconfigure(0, weight=1)
        method_frm.grid_rowconfigure(0, weight=1)
        method_frm.grid_rowconfigure(1, weight=10)
        cnt_frm.propagate(0)
        grn_frm.propagate(0)
        select_box.grid(row=0, column=0)
        cnt_frm.grid(row=1, column=0, sticky='NSEW')
        grn_frm.grid(row=1, column=0, sticky='NSEW')
        cnt_frm.tkraise()
        return method_frm
    
    def _contour_method_frame(self, master):
        self.cnt_frm = tk.Frame(master, relief='groove', borderwidth=5, bg='red')
        #img = Image.open('src/cnts.png')
        #self.cnts_img = ImageTk.PhotoImage(img)
        ex_img = tk.Label(self.cnt_frm,  height=10, width=50, bg='red')
        val_frm = tk.Frame(self.cnt_frm, height=50, bg='blue')
        thresh_entry = ttk.Entry(val_frm, textvariable=self.thresh)
        up_btn = ttk.Button(val_frm, text='▲')
        down_btn = ttk.Button(val_frm, text='▼')
        run_btn = ttk.Button(self.cnt_frm, text='RUN')
        name_lbl.pack()
        ex_img.pack()
        val_frm.pack(fill='x')
        run_btn.pack()
        return self.cnt_frm
    
    def _green_method_frame(self, master):
        self.grn_frm = tk.Frame(master, relief='groove', borderwidth=5, bg='green')
        return self.grn_frm
    
    def _select_method(self, event):
        print(event.widget.get())
        if event.widget.get() == 'Detect contours':
            self.cnt_frm.tkraise()
        else:
            self.grn_frm.tkraise()

class FvFmFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

class ArrangeFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

class ResultFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)


# GUI module
class ImageFrame(ttk.Frame):
    def __init__(self, master, out=False):
        super().__init__(master)
        lbl_frm = ttk.Frame(self, height=30)
        lbl_frm.propagate(0)
        self.img_area = tk.Label(self, relief='groove')
        self.img_area.bind('<Configure>', self._transform_frm)
        self.ratio = 0
        lbl_frm.pack(fill='x')
        self.img_area.pack(fill='both', expand=True)
        if not out:
            self.img_area.drop_target_register(dnd2.DND_FILES)
            self.img_area.dnd_bind('<<Drop>>', self._drop)
            self.filepath = tk.StringVar(value='Select File.')
            lbl = ttk.Label(lbl_frm, textvariable=self.filepath, relief='groove', font=("Calibri", 12))
            btn = ttk.Button(lbl_frm, text='▼', command=self._select_img)
            lbl.pack(side='left',fill='both', expand=True)
            btn.pack(side='left', fill='y')
        

    def _select_img(self):
        img_ext = ['*.bmp', '*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.tiff']
        path = filedialog.askopenfilename(filetypes=[('Image file', img_ext), ('All file', '*')])
        self.filepath.set(path)
        self._set_img(path)

    def _set_img(self, path):
        if path != ():
            try:
                self.img = Image.open(path)
            except:
                self.filepath.set(f'{path} is not an image file.')
                return
        else:
            return
        self.ratio = self.img.height / self.img.width
        frm_width = self.img_area.winfo_width()
        frm_height = self.img_area.winfo_height()
        self._resize_img(frm_width, frm_height)

    def _resize_img(self, new_width, new_height):
        new_ratio = new_height / new_width
        if self.ratio == 0:
            return
        if new_ratio >= self.ratio:
            new_height = new_width * self.ratio
        else:
            new_width = new_height * np.reciprocal(self.ratio)
        self.img_resized = self.img.resize((int(new_width), int(new_height)))
        self.img_resized = ImageTk.PhotoImage(self.img_resized)
        self.img_area.configure(image=self.img_resized)

    def _transform_frm(self, event):
        self._resize_img(event.width, event.height)

    def _drop(self, event):
        self.filepath.set(event.data)
        self._set_img(event.data)

# GUI module
class ScrollList(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)

# GUI module
class DropFolderFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

# File Path variable
class DropPathStringVar(tk.StringVar):
    def __init__(self):
        super().__init__()

def test():
    a = Application()
    #input_frm = InputImageFrame(a.main_frm)
    #a.test_add(input_frm, 'Input')
    a.start()
    

if __name__ == '__main__':
    #main()
    test()
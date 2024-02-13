import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np
import tkinterdnd2 as dnd2
from detect import Detect
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
        self.d = Detect()
        self.thresh = tk.StringVar()
        self.thresh.set(self.d.bin_thr)
        self.min_h = tk.StringVar()
        self.min_h.set(self.d.hsv_min[0])
        self.max_h = tk.StringVar()
        self.max_h.set(self.d.hsv_max[0])
        self._set_style()
        img_frm = self._image_frame()
        method_frm = self._method_frame()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        img_frm.grid_propagate(0)
        method_frm.grid_propagate(0)
        img_frm.grid(row=0, column=0, sticky='NSEW')
        method_frm.grid(row=0, column=1, sticky='NSEW')

    def _image_frame(self):
        img_frm = ttk.Frame(self)
        input_frm = ttk.Frame(img_frm)
        output_cnt_frm = ttk.Frame(img_frm)
        output_grn_frm = ttk.Frame(img_frm)
        self.input_frm = ImageFrame(input_frm)
        img = Image.open('src/arrow.png')
        img = img.resize((48,48))
        self.img = ImageTk.PhotoImage(img)
        space_frm = ttk.Frame(img_frm, height=30)
        arrow = tk.Label(img_frm, image=self.img)
        self.output_cnt_frm = ImageFrame(output_cnt_frm, out=True)
        self.output_green_frm = ImageFrame(output_grn_frm, out=True)
        img_frm.grid_columnconfigure(0, weight=1)
        img_frm.grid_rowconfigure(0, weight=1)
        img_frm.grid_rowconfigure(3, weight=1)
        #img_frm.grid_rowconfigure(3, weight=1)
        input_frm.grid(row=0, column=0, sticky='NSEW')
        space_frm.grid(row=1, column=0)
        arrow.grid(row=2, column=0)
        output_cnt_frm.grid(row=3, column=0, sticky='NSEW')
        output_grn_frm.grid(row=3, column=0, sticky='NSEW')
        #self.output_green_frm.grid(row=3, column=0, sticky='NSEW')
        output_cnt_frm.tkraise()
        self.input_frm.propagate(0)
        self.output_cnt_frm.propagate(0)
        self.input_frm.pack(fill='both', expand=True)
        self.output_cnt_frm.pack(fill='both', expand=True)
        self.output_green_frm.pack(fill='both', expand=True)
        return img_frm
    
    def _set_style(self):
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure('btn.TButton', font=('Calibri', 20))
        self.style.configure('lbl.TLabel', font=('Calibri', 16))

    def _method_frame(self):
        method_frm = ttk.Frame(self)
        method_lbl = ttk.Label(method_frm, text='Method', style='lbl.TLabel', padding=5)
        method_frm.bind('<Configure>', self._new_line)
        methods = ('Detect contours', 'Extract Green area')
        self.method = tk.StringVar()
        self.method.set('Detect contours')
        select_box = ttk.Combobox(method_frm, state='readonly', values=methods, font=('Calibri', 14), width= 20, justify='center', textvariable=self.method)
        select_box.option_add('*TCombobox*Listbox.Font', ('Calibri', 14))
        select_box.set('Detect contours')
        select_box.bind('<<ComboboxSelected>>', self._select_method)
        cnt_frm = self._contour_method_frame(method_frm)
        grn_frm = self._green_method_frame(method_frm)
        run_btn = ttk.Button(method_frm, text='RUN', padding=5, style='btn.TButton', command=self._run)
        next_btn = ttk.Button(method_frm, text='Next→', style='btn.TButton')
        method_frm.grid_columnconfigure(0, weight=1)
        method_frm.grid_rowconfigure(2, weight=1)
        method_lbl.grid(row=0, column=0)
        select_box.grid(row=1, column=0)
        cnt_frm.grid(row=2, column=0, sticky='NSEW')
        grn_frm.grid(row=2, column=0, sticky='NSEW')
        run_btn.grid(row=3, column=0)
        next_btn.grid(row=4, column=0, sticky='E')
        cnt_frm.tkraise()
        return method_frm
    
    def _contour_method_frame(self, master):
        self.cnt_frm = ttk.Frame(master, relief='groove', borderwidth=5)
        self.explain_cnt_lbl = ttk.Label(self.cnt_frm, padding=5, style='lbl.TLabel',text='Detects contours from an image. If it does not work well, adjust the threshold value.')
        #img = Image.open('src/cnts.png')
        #self.cnts_img = ImageTk.PhotoImage(img)
        ex_img = tk.Label(self.cnt_frm,  height=15, width=50, bg='red')
        thresh_img = tk.Label(self.cnt_frm, height=5, width=50, bg='blue')
        thresh_frm = tk.Frame(self.cnt_frm, height=50, width=80)
        thresh_frm.propagate(0)
        thresh_box = tk.Spinbox(thresh_frm, from_=0, to=255, increment=1, width=4, font=('Calibri', 14), textvariable=self.thresh)
        self.explain_cnt_lbl.pack()
        ex_img.pack()
        thresh_img.pack()
        thresh_frm.pack()
        thresh_box.pack(fill='y', expand=True)
        return self.cnt_frm
    
    def _green_method_frame(self, master):
        self.grn_frm = ttk.Frame(master, relief='groove', borderwidth=5)
        self.explain_grn_lbl = ttk.Label(self.grn_frm, padding=5, style='lbl.TLabel', text='Extract the green range. Adjust the value to set the range of colors to be extracted.')
        ex_img =tk.Label(self.grn_frm, height=15, width=50, bg='blue')
        range_img = tk.Label(self.grn_frm, height=5, width=50, bg='green')
        range_frm = tk.Frame(self.grn_frm)
        min_h_box = tk.Spinbox(range_frm, from_=0, to=180, increment=1, width=4, font=('Calibri', 14), textvariable=self.min_h)
        max_h_box = tk.Spinbox(range_frm, from_=0, to=180, increment=1, width=4, font=('Calibri', 14), textvariable=self.max_h)
        dash = ttk.Label(range_frm, text='~', style='lbl.TLabel', padding=5)
        self.explain_grn_lbl.pack()
        ex_img.pack()
        range_img.pack()
        range_frm.pack()
        min_h_box.pack(side='left', fill='y')
        dash.pack(side='left')
        max_h_box.pack(side='left', fill='y')
        return self.grn_frm
    
    def _new_line(self, event):
        width = event.width
        self.explain_cnt_lbl.configure(wraplength=width)
        self.explain_grn_lbl.configure(wraplength=width)
    
    def _select_method(self, event):
        if event.widget.get() == 'Detect contours':
            self.cnt_frm.tkraise()
            self.output_cnt_frm.tkraise()
        else:
            self.grn_frm.tkraise()
            self.output_green_frm.tkraise()

    def _run(self):
        thresh = int(self.thresh.get())
        min_hsv = self.d.hsv_min
        min_hsv[0] = int(self.min_h.get())
        max_hsv = self.d.hsv_max
        max_hsv[0] = int(self.max_h.get())
        self.d.set_param(bin_thr=thresh, hsv_max=max_hsv, hsv_min=min_hsv)
        path = self.input_frm.get_path()
        try:
            if self.method.get() == 'Detect contours':
                self.res_cnt, main_obj = self.d.extr_leaf(path)
                img = cv2.cvtColor(self.res_cnt, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                self.output_cnt_frm.set(img)
                print('contours daze!')
            elif self.method.get() == 'Extract Green area':
                print('Green dayo')
            else:
                messagebox.showerror('Method Error', 'Could not recognize the method. Please select again.')
        except (TypeError, ValueError) as e:
            messagebox.showerror('Error', e)


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
        self.path = ''
        lbl_frm = ttk.Frame(self, height=30)
        lbl_frm.propagate(0)
        self.img_area = tk.Label(self, relief='groove')
        self.img_area.propagate(0)
        self.img_area.bind('<Configure>', self._transform_frm)
        self.ratio = 0
        lbl_frm.pack(fill='x')
        self.img_area.pack(fill='both', expand=True)
        if not out:
            self.img_area.drop_target_register(dnd2.DND_FILES)
            self.img_area.dnd_bind('<<Drop>>', self._drop)
            self.text_var = tk.StringVar(value='Select file')
            lbl = ttk.Label(lbl_frm, textvariable=self.text_var, relief='groove', font=("Calibri", 12))
            btn = ttk.Button(lbl_frm, text='▼', command=self._select_img)
            lbl.pack(side='left',fill='both', expand=True)
            btn.pack(side='left', fill='y')
        

    def _select_img(self):
        img_ext = ['*.bmp', '*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.tiff']
        self.path = filedialog.askopenfilename(filetypes=[('Image file', img_ext), ('All file', '*')])
        self.text_var.set(self.path)
        self._set_img(self.path)

    def _set_img(self, path):
        if path != ():
            try:
                self.img = Image.open(path)
            except:
                self.text_var.set(f'{path} is not an image file.')
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
        self.path = event.data
        self.text_var.set(event.data)
        self._set_img(event.data)

    def get_path(self):
        return self.path
    
    def set(self, img):
        self.img = img
        self.ratio = self.img.height / self.img.width
        frm_width = self.img_area.winfo_width()
        frm_height = self.img_area.winfo_height()
        self._resize_img(frm_width, frm_height)

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
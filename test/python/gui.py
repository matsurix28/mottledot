import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np
import tkinterdnd2 as dnd2
from detect import Detect
from fvfm import Fvfm
from PIL import Image, ImageTk


def main():
    app = Application()
    app.start()

class Application():
    def __init__(self) -> None:
        self.root = dnd2.Tk()
        self.root.geometry('1000x700')
        self.root.wm_minsize(1080, 700)
        self.root.title('Pickcell Color')
        self.main_frm = MainFrame(self.root)

    def _set_vars(self):
        self.grn_path = None
        self.fvfm_path = None
        self.main_obj = None

    def start(self):
        #self.detect_frm = DetectFrame(self.root, self)
        #self.main_frm.add_tab(self.detect_frm, 'Detect leaf')
        #self.fvfm_frm = FvFmFrame(self.root, self)
        #self.main_frm.add_tab(self.fvfm_frm, 'Fv/Fm value')
        self.arrange_frm = ArrangeFrame(self.root)
        self.main_frm.add_tab(self.arrange_frm, 'Arrange')
        self.result_frm = ResultFrame(self.root)
        self.main_frm.add_tab(self.result_frm, 'Result')
        self.root.mainloop()

    def test_add(self, frame, title):
        self.main_frm.add_tab(frame, title)

#    def d2f(self):
#        self.grn_path, self.grn_img, self.grn_cnt = self.detect_frm.get()
#        self.main_frm.notebook.select(self.fvfm_frm)

#    def f2a(self):
#        self.main_frm.notebook.select(self.arrange_frm)
    
#    def res_detect(self):
#        self.grn_path, self.grn_img, self.grn_cnt = self.detect_frm.get()
#        self.arrange_frm.set_grn(self.grn_img, self.grn_cnt)

#    def res_fvfm(self):
#        self.fvfm_path, self.fvfm_img, self.fvfm_cnt, self.fvfm_list = self.fvfm_frm.get()
#        self.arrange_frm.set_fvfm(self.fvfm_img, self.fvfm_cnt)

class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
    
    def add_tab(self, frame, title):
        self.notebook.add(frame, text=title)

class DetectFrame(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, relief='groove', borderwidth=10)
        self.app = app
        self.d = Detect()
        self._set_vars()
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

    def _set_vars(self):
        self.path = None
        self.def_min_h = self.d.hsv_min[0]
        self.def_max_h = self.d.hsv_max[0]
        self.def_thresh = self.d.bin_thr
        self.thresh = tk.StringVar()
        self.thresh.set(self.def_thresh)
        self.thresh.trace('w', self._thresh_bar)
        self.min_h = tk.StringVar()
        self.min_h.set(self.def_min_h)
        self.min_h.trace('w', self._hue_bar)
        self.max_h = tk.StringVar()
        self.max_h.set(self.def_max_h)
        self.max_h.trace('w', self._hue_bar)
        self.progress_var = tk.StringVar()
        self.res_img = None
        self.main_obj = None

    def _image_frame(self):
        img_frm = ttk.Frame(self)
        self.input_frm = ImageFrame(img_frm)
        img = Image.open('src/arrow.png')
        img = img.resize((48,48))
        self.img = ImageTk.PhotoImage(img)
        space_frm = ttk.Frame(img_frm, height=30)
        self.arrow = tk.Label(img_frm, image=self.img, textvariable=self.progress_var, compound='center', font=('Calibri', 14))
        self.output_cnt_frm = ImageFrame(img_frm, out=True)
        self.output_grn_frm = ImageFrame(img_frm, out=True)
        img_frm.grid_columnconfigure(0, weight=1)
        img_frm.grid_rowconfigure(0, weight=1)
        img_frm.grid_rowconfigure(3, weight=1)
        self.input_frm.grid(row=0, column=0, sticky='NSEW')
        space_frm.grid(row=1, column=0)
        self.arrow.grid(row=2, column=0)
        self.output_cnt_frm.grid(row=3, column=0, sticky='NSEW')
        self.output_grn_frm.grid(row=3, column=0, sticky='NSEW')
        self.output_grn_frm.grid(row=3, column=0, sticky='NSEW')
        self.output_cnt_frm.tkraise()
        self.input_frm.propagate(0)
        self.output_cnt_frm.propagate(0)
        self.output_grn_frm.propagate(0)
        return img_frm
    
    def _set_style(self):
        style = ttk.Style()
        style.theme_use('classic')
        style.configure('btn.TButton', font=('Calibri', 16))
        style.configure('lbl.TLabel', font=('Calibri', 14))

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
        next_btn = ttk.Button(method_frm, text='Next→', style='btn.TButton', command=self._next)
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
    
    def get(self):
        return self.path, self.res_img, self.main_obj

    def _contour_method_frame(self, master):
        self.cnt_frm = ttk.Frame(master, relief='groove', borderwidth=5)
        self.explain_cnt_lbl = ttk.Label(self.cnt_frm, padding=5, style='lbl.TLabel',text='Detects contours from an image. If it does not work well, adjust the threshold value. (Threshold range is 0-255)')
        #img = Image.open('src/cnts.png')
        #self.cnts_img = ImageTk.PhotoImage(img)
        ex_img = tk.Frame(self.cnt_frm,  height=200, width=450, bg='red')
        setting_frm = tk.Frame(self.cnt_frm)
        thresh_lbl = ttk.Label(setting_frm, text='Threshold', style='lbl.TLabel')
        self.thresh_img = tk.Label(setting_frm)
        self._thresh_bar()
        thresh_frm = tk.Frame(setting_frm, height=50, width=80)
        thresh_frm.propagate(0)
        thresh_box = tk.Spinbox(thresh_frm, from_=0, to=255, increment=1, width=4, font=('Calibri', 14), textvariable=self.thresh)
        reset_frm = tk.Frame(setting_frm, width=450, height=50)
        reset_btn = ttk.Button(setting_frm, text='Reset', command=self._reset_thresh, style='btn.TButton')
        self.cnt_frm.grid_columnconfigure(0, weight=1)
        self.cnt_frm.grid_rowconfigure(0, weight=1)
        self.cnt_frm.grid_rowconfigure(1, weight=1)
        self.cnt_frm.grid_rowconfigure(2, weight=1)
        self.cnt_frm.grid_rowconfigure(3, weight=1)
        self.explain_cnt_lbl.grid(row=0, column=0)
        ex_img.grid(row=1, column=0)
        setting_frm.grid(row=2, column=0)
        thresh_lbl.grid(row=0, column=0)
        self.thresh_img.grid(row=1, column=0)
        #reset_frm.grid(row=2, column=0)
        thresh_frm.grid(row=2, column=0)
        #reset_frm.pack_propagate(0)
        thresh_box.pack(fill='y', expand=True)
        #reset_btn.pack(side='right')
        reset_btn.grid(row=2, column=0, sticky='E')
        thresh_frm.tkraise()
        return self.cnt_frm
    
    def _green_method_frame(self, master):
        self.grn_frm = tk.Frame(master, relief='groove', borderwidth=5)
        self.explain_grn_lbl = ttk.Label(self.grn_frm, padding=5, style='lbl.TLabel', text='Extract the green range. Adjust the value to set the range of colors to be extracted. (Hue range is 0-180.)')
        ex_img =tk.Frame(self.grn_frm, height=200, width=450, bg='blue')
        self.range_img = tk.Label(self.grn_frm)
        self._hue_bar()
        frm = tk.Frame(self.grn_frm, width=450, height=50)
        range_frm = tk.Frame(frm)
        min_h_box = tk.Spinbox(range_frm, from_=0, to=180, increment=1, width=4, font=('Calibri', 14), textvariable=self.min_h)
        max_h_box = tk.Spinbox(range_frm, from_=0, to=180, increment=1, width=4, font=('Calibri', 14), textvariable=self.max_h)
        dash = ttk.Label(range_frm, text='~', style='lbl.TLabel', padding=5)
        reset_frm = tk.Frame(self.grn_frm, width=450, height=50)
        reset_btn = ttk.Button(reset_frm, text='Reset', command=self._reset_hue, style='btn.TButton')
        #self.explain_grn_lbl.pack()
        #ex_img.pack()
        #self.range_img.pack()
        #frm.pack()
        #frm.propagate(0)
        self.grn_frm.grid_columnconfigure(0, weight=1)
        self.explain_grn_lbl.grid(row=0, column=0)
        ex_img.grid(row=1, column=0)
        self.range_img.grid(row=2, column=0)
        frm.grid(row=3, column=0, )
        range_frm.pack()
        min_h_box.pack(side='left', fill='y')
        dash.pack(side='left')
        max_h_box.pack(side='left', fill='y')
        #reset_btn.pack(after= range_frm, side='right')
        reset_frm.grid(row=3, column=0)
        reset_frm.propagate(0)
        reset_btn.pack(side='right')
        frm.tkraise()
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
            self.output_grn_frm.tkraise()

    def _reset_thresh(self):
        self.thresh.set(self.def_thresh)

    def _reset_hue(self):
        self.min_h.set(self.def_min_h)
        self.max_h.set(self.def_max_h)

    def _run(self):
        self.path = self.input_frm.get_path()
        try:
            if self.method.get() == 'Detect contours':
                if self.thresh.get() == '':
                    self.thresh.set(0)
                thresh = int(self.thresh.get())
                self.d.set_param(bin_thr=thresh)
                self.progress_var.set('Detecting contours...')
                self.arrow.update()
                self.res_img, self.main_obj = self.d.extr_leaf(self.path)
                img = cv2.cvtColor(self.res_img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                self.output_cnt_frm.set(img)
            elif self.method.get() == 'Extract Green area':
                if self.min_h.get() == '':
                    self.min_h.set(0)
                if self.max_h.get() == '':
                    self.max_h.set(0)
                if int(self.min_h.get()) > int(self.max_h.get()):
                    print('gyaku gyaku')
                    min = int(self.max_h.get())
                    max = int(self.min_h.get())
                else:
                    min = int(self.min_h.get())
                    max = int(self.max_h.get())
                min_hsv = self.d.hsv_min
                min_hsv[0] = min
                max_hsv = self.d.hsv_max
                max_hsv[0] = max
                print('settei atai', min_hsv, max_hsv)
                self.d.set_param(hsv_min=min_hsv, hsv_max=max_hsv)
                self.progress_var.set('Extracting a specified color range...')
                self.arrow.update()
                self.res_img, self.main_obj = self.d.extr_green(self.path)
                img = cv2.cvtColor(self.res_img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                self.output_grn_frm.set(img)
            else:
                messagebox.showerror('Method Error', 'Could not recognize the method. Please select again.')
        except (TypeError, ValueError) as e:
            if self.method.get() == 'Detect contours':
                self.output_cnt_frm.clear()
            elif self.method.get() == 'Extract Green area':
                self.output_grn_frm.clear()
            messagebox.showerror('Error', e)
        self.progress_var.set('')

    def _hue_bar(self, *args):
        if self.max_h.get() == '' or self.min_h.get() == '':
            return
        if int(self.min_h.get()) > 180:
            self.min_h.set(180)
        if int(self.min_h.get()) < 0:
            self.min_h.set(0)
        if int(self.max_h.get()) > 180:
            self.max_h.set(180)
        if int(self.max_h.get()) < 0:
            self.max_h.set(0)
        low = [int(self.min_h.get()), 50, 50]
        high = [int(self.max_h.get()), 255,200]
        height = 70
        width = 450
        img = np.zeros((height, width, 3), np.uint8)
        h = np.linspace(low[0], high[0], width)
        s = np.linspace(low[1], high[1], height)
        v = np.linspace(low[2], high[2], height)
        for i in range(width):
            for j in range(height):
                img[j,i,0] = h[i]
                img[j,i,1] = s[j]
                img[j,i,2] = v[j]
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        img = Image.fromarray(img)
        self.hue_img = ImageTk.PhotoImage(img)
        self.range_img.configure(image=self.hue_img)

    def _thresh_bar(self, *args):
        if self.thresh.get() == '':
            return
        if int(self.thresh.get()) > 255:
            self.thresh.set(255)
        elif int(self.thresh.get()) < 0:
            self.thresh.set(0)
        low = int(self.thresh.get())
        high = 255
        height = 70
        width = 400
        img = np.zeros((height, width, 1), np.uint8)
        thresh = np.linspace(low, high, width)
        for i in range(width):
            for j in range(height):
                img[j,i,0] = thresh[i]
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = Image.fromarray(img)
        self.thresh_bar_img = ImageTk.PhotoImage(img)
        self.thresh_img.configure(image=self.thresh_bar_img)

    def _next(self):
        if (self.path is not None) and (self.res_img is not None) and (self.main_obj is not None):
            self.app.d2f()

class FvFmFrame(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.d = Detect()
        self.f = Fvfm()
        self._set_var()
        self._set_str()
        self._set_style()
        self._create_widgets()

    def _set_str(self):
        self.explain_msg = (
            'Reads the Fv/Fm scale bar from an image and creates '
            'its value and color correspondence table. Also, extract '
            'only the leaf area from an image.'
        )

    def _set_var(self):
        self.input_frm = None
        self.arrow = None
        self.output_frm = None
        self.arrow_img = None
        self.progress_msg = tk.StringVar()
        self.list_frm = None
        self.fvfm_val_list = None
        self.fvfm_img_lsit = None
        self.def_thresh = self.d.bin_thr
        self.thresh = tk.StringVar()
        self.thresh.set(self.def_thresh)
        self.path = None

    def _set_style(self):
        style = ttk.Style()
        style.theme_use('classic')
        style.configure('lbl.TLabel', font=('Calibri', 16))

    def _create_widgets(self):
        img_frm = self._image_frame()
        list_frm = self._value_list_frame()
        method_frm = self._method_frame()
        img_frm.grid(column=0, row=0, sticky='NSEW')
        list_frm.grid(column=1, row=0, sticky='NSEW')
        method_frm.grid(column=2, row=0, sticky='NSEW')
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=1)

    def _image_frame(self):
        # <Widgets> ------------------------------
        frm = ttk.Frame(self)
        self.input_frm = ImageFrame(frm)
        space_frm = ttk.Frame(frm, height=30)
        self.arrow = tk.Label(frm)
        self.output_frm = ImageFrame(frm, out=True)
        # </Widgets> ------------------------------
        # <Configure> -----------------------------
        # arrow
        img = Image.open('src/arrow.png')
        img = img.resize((48,48))
        self.arrow_img = ImageTk.PhotoImage(img)
        self.arrow.configure(
            image=self.arrow_img, 
            textvariable=self.progress_msg, 
            compound='center', 
            font=('Calibri', 14)
            )
        # <Layouts> -------------------------------
        self.input_frm.grid(column=0, row=0, sticky='NSEW')
        space_frm.grid(column=0, row=1)
        self.arrow.grid(column=0, row=2)
        self.output_frm.grid(column=0, row=3, sticky='NSEW')
        frm.grid_columnconfigure(0, weight=1)
        frm.grid_rowconfigure(0, weight=1)
        frm.grid_rowconfigure(3, weight=1)
        self.input_frm.propagate(0)
        self.output_frm.propagate(0)
        frm.grid_propagate(0)
        # </Layouts> ------------------------------
        return frm

    def _value_list_frame(self):
        # <Widgets> ------------------------------
        frm = ttk.Frame(self)
        title_lbl = ttk.Label(frm)
        list_frm = ttk.Frame(frm)
        self.list_frm = ScrollList(list_frm)
        # </Widgets> -----------------------------
        # <Configure> ----------------------------
        title_lbl.configure(
            text='Fv/Fm value list',
            style='lbl.TLabel'
            )
        # </Configure> ---------------------------
        # <Layouts> ------------------------------
        title_lbl.pack()
        list_frm.pack(fill='both', expand=True)
        frm.pack_propagate(0)
        # </Layouts> -----------------------------
        #self.test()
        return frm

    def test(self):
        iro = [[0,74,255],[0,136,255], [0,189,255], [28,255,14], [238,255,119],[0,74,255],[0,136,255], [0,189,255], [28,255,14], [238,255,119],[0,74,255],[0,136,255], [0,189,255], [28,255,14], [238,255,119],[0,74,255],[0,136,255], [0,189,255], [28,255,14], [238,255,119],[0,74,255],[0,136,255], [0,189,255], [28,255,14], [238,255,119],[0,74,255],[0,136,255], [0,189,255], [28,255,14], [238,255,119]]
        val = [832.0, 825.0, 820.0, 800.0, 790.0,832.0, 825.0, 820.0, 800.0, 790.0,832.0, 825.0, 820.0, 800.0, 790.0,832.0, 825.0, 820.0, 800.0, 790.0,832.0, 825.0, 820.0, 800.0, 790.0,832.0, 825.0, 820.0, 800.0, 790.0]
        self.imgs = []
        for color in iro:
            img = np.full((36,36,3), color, np.uint8)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.imgs.append(img)
        self.list_frm.set_list(self.imgs, val)

    def _method_frame(self):
        # <Widgets> -------------------------------
        frm = tk.Frame(self)
        title_lbl = ttk.Label(frm)
        explain_txt = ttk.Label(frm)
        ex_img = tk.Frame(frm, width=400, height=200, bg='red')
        settings_frm = ttk.Frame(frm)
        thresh_lbl = ttk.Label(settings_frm)
        self.thresh_img = tk.Label(settings_frm)
        thresh_frm = tk.Frame(settings_frm)
        thresh_spinbox = tk.Spinbox(thresh_frm)
        reset_btn = ttk.Button(settings_frm)
        btn_frm = ttk.Frame(frm)
        run_btn = ttk.Button(btn_frm)
        next_btn = ttk.Button(btn_frm)
        # </Widget> -------------------------------
        # <Configure> -----------------------------
        title_lbl.configure(
            text='Method', 
            style='lbl.TLabel'
            )
        explain_txt.configure(text=self.explain_msg, style='lbl.TLabel')
        thresh_lbl.configure(text='Threshold', state='lbl.TLabel')
        self._thresh_bar()
        thresh_frm.configure(height=50, width=80)
        thresh_spinbox.configure(
            from_=0, to=255, increment=1, 
            width=4, 
            font=('Calibri', 14), 
            textvariable=self.thresh
        )
        reset_btn.configure(
            text='Reset', 
            style='btn.TButton', 
            command=self._reset_thr
            )
        run_btn.configure(
            text='RUN',
            style='btn.TButton',
            command=self._run
        )
        next_btn.configure(
            text='NEXT',
            style='btn.TButton',
            command=self._next
        )
        # </Configure> ----------------------------
        # <Layouts> -------------------------------
        title_lbl.grid(column=0, row=0)
        explain_txt.grid(column=0, row=1)
        ex_img.grid(column=0, row=2)
        settings_frm.grid(column=0, row=3)
        # Inner settins_frm ------------------->
        thresh_lbl.grid(column=0, row=0)
        self.thresh_img.grid(column=0, row=1)
        thresh_frm.grid(column=0, row=2)
        # Inner thresh_frm ---------->>
        thresh_spinbox.pack(fill='y', expand=True)
        # --------------------------->>
        # ------------------------------------->>
        reset_btn.grid(column=0, row=2, sticky='E')
        btn_frm.grid(column=0, row=4, sticky='SEW')
        # inner btn_frm ---------->
        run_btn.pack()
        next_btn.pack(side='right')
        frm.grid_columnconfigure(0, weight=1)
        frm.grid_rowconfigure(2, weight=1)
        frm.grid_rowconfigure(3, weight=1)
        frm.grid_propagate(0)
        thresh_frm.propagate(0)
        return frm

    def _reset_thr(self):
        self.thresh.set(self.def_thresh)

    def _thresh_bar(self, *args):
        if self.thresh.get() == '':
            return
        if int(self.thresh.get()) > 255:
            self.thresh.set(255)
        elif int(self.thresh.get()) < 0:
            self.thresh.set(0)
        low = int(self.thresh.get())
        high = 255
        height = 70
        width = 400
        img = np.zeros((height, width, 1), np.uint8)
        thresh = np.linspace(low, high, width)
        for i in range(width):
            for j in range(height):
                img[j,i,0] = thresh[i]
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = Image.fromarray(img)
        self.thresh_bar_img = ImageTk.PhotoImage(img)
        self.thresh_img.configure(image=self.thresh_bar_img)

    def _run(self):
        self.path = self.input_frm.get_path()
        try:
            if self.thresh.get() == '':
                self.thresh.set(0)
            thresh = int(self.thresh.get())
            self.d.set_param(bin_thr=thresh)
            self.progress_msg.set('Read Fv/Fm scale bar and detect leaf...')
            self.arrow.update()
            self.res_img, self.res_cnt = self.d.extr_leaf(self.path)
            img = cv2.cvtColor(self.res_img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.output_frm.set(img)
            self.fvfm_list = self.f.get(self.path)
            self._set_list(self.fvfm_list)
        except (TypeError, ValueError) as e:
            self.output_frm.clear()
            messagebox.showerror('Error', e)
        self.progress_msg.set('')
        self.app.res_fvfm()

    def _set_list(self, fvfm_list):
        value_list = [i[1] for i in fvfm_list]
        self.color_imgs = []
        for f in fvfm_list:
            color = f[0]
            img = np.full((36,36,3), color, np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.color_imgs.append(img)
        self.list_frm.set_list(self.color_imgs, value_list)

    def get(self):
        return self.path, self.res_img, self.res_cnt, self.fvfm_list

    def _next(self):
        if (self.path is not None) and (self.res_img is not None) and (self.res_cnt is not None) and (self.fvfm_list is not None):
            self.app.f2a()

class ArrangeFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()

    def _set_str(self):
        pass

    def _set_var(self):
        self.grn_img = None
        self.fvfm_img = None

    def set_grn(self, grn_img, grn_cnt):
        self.grn_img = grn_img
        self.grn_cnt = grn_cnt

    def set_fvfm(self, fvfm_img, fvfm_cnt):
        self.fvfm_img = fvfm_img
        self.fvfm_cnt = fvfm_cnt

    def _set_style(self):
        style = ttk.Style()
        style.theme_use('classic')
        style.configure('lbl.TLabel', font=('Calibri', 16))

    def _create_widgets(self):
        # <Widgets> -------------------------
        img_frm = tk.Frame(self, bg='red')
        grn_frm = self._green_frame(img_frm)
        fvfm_frm = self._fvfm_frame(img_frm)
        method_frm = self._method_frame()
        # </Widgets> ------------------------
        # <Configure> -----------------------
        # </Configure> ----------------------
        # <Layouts> -------------------------
        img_frm.grid(column=0, row=0, sticky='NSEW')
        grn_frm.pack()
        fvfm_frm.pack()
        method_frm.grid(column=1, row=0, sticky='NSEW')
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _green_frame(self, master):
        frm = ttk.Frame(master)
        in_grn_frm = ImageFrame(frm)
        arrow = ttk.Label(frm)
        out_grn_frm = ImageFrame(frm, out=True)
        in_grn_frm.grid(column=0, row=0, sticky='NSEW')
        arrow.grid(column=1, row=0)
        out_grn_frm.grid(column=2, row=0, sticky='NSEW')
        frm.grid_columnconfigure(0, weight=1)
        frm.grid_columnconfigure(2, weight=1)
        frm.grid_propagate(0)
        return frm

    def _fvfm_frame(self, master):
        frm = ttk.Frame(master)
        in_fvfm_frm = ImageFrame(frm)
        fvfm_arrow = ttk.Label(frm)
        out_fvfm_frm = ImageFrame(frm, out=True)
        return frm

    def _method_frame(self):
        frm = tk.Frame(self, bg='blue')
        return frm


class ResultFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)


# GUI module
class ImageFrame(ttk.Frame):
    def __init__(self, master, out=False):
        super().__init__(master)
        self.path = ''
        self.img = None
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
        if self.img is None:
            return
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

    def clear(self):
        print('clear')
        self.img = None
        self.img_resized = None

# GUI module
class ScrollList(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)
        self._set_style()
        self._create_widgets()

    def _set_style(self):
        style = ttk.Style()
        style.theme_use('classic')
        style.configure('lbl.TLabel', font=('Calibri', 14))

    def _create_widgets(self):
        # <Widgets> -------------------------------
        self.frame = ttk.Frame(self)
        scroll_bar = ttk.Scrollbar(self)
        # </Widgets> ------------------------------
        # <Configure> -----------------------------
        # self
        self.configure(
            scrollregion=(0,0,0,0),
            yscrollcommand=scroll_bar.set
        )
        # scroll_bar
        scroll_bar.configure(
            orient='vertical',
            command=self.yview
        )
        #self.create_window()
        self.create_window((0,0), window=self.frame, anchor='nw')
        # frame
        self.frame.bind('<Configure>', self._set_scrollregion)
        # </Configure> ----------------------------
        # <Layouts> -------------------------------
        self.pack(fill='both', expand=True)
        scroll_bar.pack(side='right', fill='y')
        self.pack_propagate(0)
        # </Layouts> ------------------------------

    def set_list(self, img_list, val_list):
        if len(img_list) != len(val_list):
            raise ValueError('The length of the list is incorrect.')
        for (img, val) in zip(img_list, val_list):
            lbl = ttk.Label(
                self.frame, 
                text=val,
                image=img,
                compound='left',
                style='lbl.TLabel'
                )
            lbl.pack(fill='x', expand=True)

    def _set_scrollregion(self, event):
        height = self.frame.winfo_height()
        print(height)
        self.configure(scrollregion=(0,0,0,height))

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
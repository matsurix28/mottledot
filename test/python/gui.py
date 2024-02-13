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
        super().__init__(master)

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
class InputImageFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        lbl_frm = ttk.Frame(self)
        self.img_area = tk.Label(self, relief='groove')
        self.img_area.bind('<Configure>', self._transform_frm)
        self.img_area.drop_target_register(dnd2.DND_FILES)
        self.img_area.dnd_bind('<<Drop>>', self._drop)
        self.ratio = 0
        lbl_frm.pack(fill='x')
        self.img_area.pack(fill='both', expand=True)
        self.filepath = tk.StringVar(value='Select File.')
        lbl = ttk.Label(lbl_frm, textvariable=self.filepath, relief='groove')
        btn = ttk.Button(lbl_frm, text='▼', command=self._get_path)
        btn.pack(side='right')
        lbl.pack(fill='x')

    def _get_path(self):
        img_ext = ['*.bmp', '*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.tiff']
        path = filedialog.askopenfilename(filetypes=[('Image file', img_ext), ('All file', '*')])
        self.filepath.set(path)
        self._set_img(path)

    def _set_img(self, path):
        self.img = Image.open(path)
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
        self.img_area.configure(image=self.img_resized, compound='center')

    def _transform_frm(self, event):
        self._resize_img(event.width, event.height)

    def _drop(self, event):
        print(event.data)

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
    input_frm = InputImageFrame(a.main_frm)
    a.test_add(input_frm, 'Input')
    a.start()

if __name__ == '__main__':
    #main()
    test()
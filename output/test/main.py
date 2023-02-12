from tkinter import *
import cv2
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
import os, json
from PIL import ImageTk, Image
import os

def img_src(src, imgsize):
    try:
        openimg = ImageTk.Image.open(src)
        w, h = openimg.size
        if sum(imgsize) > 1:
            openimg = openimg.resize(imgsize, Image.CUBIC)
        timg = ImageTk.PhotoImage(openimg)
        return timg
    except Exception as e:
        showerror("Error", str(e))

root = Tk()
root.geometry('124x124')
root.title('test')
root.wm_resizable(height=False,width=False)
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
frame=Frame(root,bg='#F1F1F1',height=124,width=124).place(x=0,y=0)

root.mainloop()
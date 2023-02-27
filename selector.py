#! /bin/python3
# install tkinter
# sudo dnf install python3-tkinter
# sudo dnf install python3-pillow
# sudo dnf install python3-pillow-tk

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image 
#from pillow import ImageTk 
from PIL import ImageTk

import os
import shutil

import argparse

class Controller:

  bordersize = 20

  def __init__(self, inpath, suffix, outpath, keep_default):
    # View
    self.root = Tk()
    #self.frame = ttk.Frame(root, padding=10)
    self.img = Canvas(self.root, highlightthickness = self.bordersize)
    self.image = None
    self.photoimage = None

    # Paths
    if not inpath.endswith('/'):
      self.inpath = inpath + '/'
    else:
      self.inpath = inpath

    if not outpath.endswith('/'):
      self.outpath = outpath+'/'
    else:
      self.outpath = outpath

    self.suffix = suffix

    # Data
    self.imgs = []
    self.current = 0
    self.keep_default = keep_default


    #self.frame.grid()
    self.root.bind("<Right>", self.next_image)
    self.root.bind("<Left>", self.last_image)
    self.root.bind("<Up>", self.keep_image)
    self.root.bind("<Down>", self.remove_image)
    self.root.bind("i", self.show_info)
    self.root.bind("w", self.copy_files)
    self.root.bind("h", self.show_help)
    #self.img.grid(column=0, row=0)
    self.root.geometry("1024x712")
    self.img.bd = self.bordersize
    self.load_data()
    self.present_image(0)

  def load_data(self):
    for name in sorted(os.listdir(self.inpath)):
      if name.lower().endswith(self.suffix.lower()) and os.path.isfile(self.inpath + name):
        self.imgs.append([name, self.keep_default, False])

  def all_visited(self):
    for entry in self.imgs:
      if not entry[2]:
        return False
    return True

  def copy_files(self, event):
    keep_text = "be copied like kept files"
    if not self.keep_default:
      keep_text = "not be copied"
    if not self.all_visited() and not messagebox.askyesno("Not all files reviewed", "You have not reviewed all files so far. Unseen files will "+keep_text+". Do you still want to proceed?"):
        return
    
    # copy files
    if not os.path.exists(self.outpath):
      os.mkdir(self.outpath)
    for image in self.imgs:
      if image[1]:
        shutil.copy2(self.inpath+image[0], self.outpath+image[0])
    messagebox.showinfo("Done", "All files marked as 'keep' (white border) were copied to the directory "+self.outpath+"\nYou may now close this program.")

  def present_image(self, index):
    self.current = index 
    # set visited
    self.imgs[self.current][2] = True
    # check keep value
    if not self.imgs[self.current][1]:
      self.img.config(bg = 'red', highlightbackground = 'red', highlightcolor = 'red')
    else:
      self.img.config(bg = 'white', highlightbackground = 'white', highlightcolor = 'white')
    self.image = Image.open(self.inpath+self.imgs[self.current][0])
    w = self.root.winfo_width()-self.bordersize
    h = self.root.winfo_height()-self.bordersize
    if w < 10:
      w = 10
    if h < 10:
      h = 10
    self.image = self.image.resize((w, h), Image.Resampling.NEAREST)
    self.img.width = self.image.size[0]
    self.img.height = self.image.size[1]
    self.photoimage = ImageTk.PhotoImage(self.image)
    self.img.create_image(0, 0, anchor = NW, image = self.photoimage)
    self.img.pack(fill=BOTH, expand=1)#, padx=self.bordersize, pady=self.bordersize)

  def next_image(self, event):
    index = 0
    if self.current+1 < len(self.imgs):
      index = self.current+1
    self.present_image(index)
    if index == 0 and self.all_visited():
      messagebox.showinfo("All images visited", "You have reviewed all images! You can copy selected Images by using 'w'.")

  def last_image(self, event):
    index = len(self.imgs)-1
    if self.current-1 >= 0:
      index = self.current-1
    self.present_image(index)

  def keep_image(self, event):
    self.imgs[self.current][1] = True
    self.present_image(self.current)

  def remove_image(self, event):
    self.imgs[self.current][1] = False
    self.present_image(self.current)

  def show_info(self, event):
    messagebox.showinfo("Image Info", "Image "+str(self.current+1)+"/"+str(len(self.imgs))+"\nName: "+self.inpath+self.imgs[self.current][0])

  def show_help(self, event):
    helpstring = '''
The controlkeys are the following:\n
left/right arrow - navigation through the images; right - next, left - previous\n
up arrow - keep the current image (i.e. copy it when \'w\' is used)\n
down arrow - do not keep the current image (i.e. do not copy it)\n
i - get information about the current image\n
w - copy files as selected\n
h - print help
    '''
    messagebox.showinfo("Help", helpstring)

# Argumentparsing

parser = argparse.ArgumentParser(prog = 'selector', description = 'This small tool helps to sort out images. It assumes the files are located in one folder and you want to copy some of these files to another folder. The tool helps to select which files to keep (i.e. to copy) and which not.', \
epilog = '''
The controlkeys are the following:\n
left/right arrow - navigation through the images; right - next, left - previous\n
up arrow         - keep the current image (i.e. copy it when \'w\' is used)\n
down arrow       - do not keep the current image (i.e. do not copy it)\n
i                - get information about the current image\n
w                - copy files as selected\n
h                - print help\n
''')

parser.add_argument("inpath", help = 'path where all images are located')
parser.add_argument("outpath", help = 'path to copy selected images to')

parser.add_argument('-k', '--keep-default', dest = 'keepdefault', type = bool, default = True, help = 'states if to keep all images by default [default: True]')
parser.add_argument('-s', '--suffix', dest = 'suffix', type = str, default = 'JPG', help = 'the filename suffix of the files to select from [default: JPG]')

args = parser.parse_args()

controller = Controller(args.inpath, args.suffix, args.outpath, args.keepdefault)
controller.root.mainloop()


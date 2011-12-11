#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob;
import os;
from Tkinter import LEFT, Tk, Label, Entry;
from PIL import Image, ImageTk;

window = Tk();
textLabel = Entry(window);
imageLabel = Label(window);
files = glob.glob("../image/*.jpg");

def rename(fname, rname):
    _dir = os.path.dirname(fname);
    _name = os.path.join(_dir, rname+".png");
    print fname, _name
    os.rename(fname, _name);

def nextImage(isFirst = False):
    reName = textLabel.get();
    textLabel.delete(0, len(reName));
    fname = os.path.abspath(files[0]);
    if(not isFirst):
        if(reName):
            rename(fname, reName);
            del files[0];
            fname = os.path.abspath(files[0]);
        else:
            return;
    img = Image.open(fname);
    tkImg =ImageTk.PhotoImage(img);
    imageLabel.configure(image = tkImg);
    imageLabel.image = tkImg;
    imageLabel.pack();
    textLabel.pack(side=LEFT);

def onEnter(event):
    nextImage(False);

def main():
    textLabel.bind("<Return>", onEnter);
    nextImage(True);
    window.mainloop();

if __name__ == '__main__':
    main()

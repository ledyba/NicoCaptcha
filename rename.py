#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      psi
#
# Created:     07/12/2011
# Copyright:   (c) psi 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys;
import glob;
import os;
from Tkinter import *;
from PIL import Image, ImageTk;

window = Tk();
textLabel = Entry(window);
imageLabel = Label(window);
files = glob.glob("./image/*.jpg");

def rename(fname, rname):
    dir = os.path.dirname(fname);
    _name = os.path.join(dir, rname+".png");
    print fname, _name
    os.rename(fname, _name);

def next(isFirst = False):
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
    next(False);

def main():
    textLabel.bind("<Return>", onEnter);
    next(True);
    window.mainloop();

if __name__ == '__main__':
    main()

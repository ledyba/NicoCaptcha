#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob;
import os;
import random;
from Tkinter import LEFT, Tk, Label, Entry;
from tkFont import Font;
from PIL import Image, ImageTk;

window = Tk();
textLabel = Entry(window, font=Font(size=36,weight="bold"), width=6);
imageLabel = Label(window);
files = glob.glob("../image/*.jpg");
random.shuffle(files);


def rename(fname, rname):
	_dir = os.path.dirname(fname)+"/../renamed/";
	_name = os.path.join(_dir, rname+".png");
	cnt = 0;
	while os.path.exists(_name):
		cnt+=1;
		_name = os.path.join(_dir, rname+"_"+str(cnt)+".png");
	print fname, _name
	os.rename(fname, _name);

def nextImage(isFirst = False):
	reName = textLabel.get();
	textLabel.delete(0, len(reName));
	fname = os.path.abspath(files[0]);
	if(not isFirst):
		if(reName and len(reName)==5):
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
	textLabel.pack();

def onEnter(event):
	nextImage(False);

def main():
	textLabel.bind("<Return>", onEnter);
	nextImage(True);
	window.mainloop();

if __name__ == '__main__':
	main()

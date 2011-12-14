#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob;
import os;
import random;
from Tkinter import Tk, Label, Frame, Entry;
from tkFont import Font;
from captcha import Captcha, Trainer;
cap = None;
trainer = Trainer();

def onNext(isFirst):
	global cap, trainer;
	ans = textLabel.get();
	textLabel.delete(0, len(ans));
	fname = os.path.abspath(files[0]);
	if(not isFirst):
		if ans and len(ans) == 5:
			cap.train(ans);
			trainer.save();
		elif len(ans) == 0:
			pass
		else:
			return
		del files[0];
		fname = os.path.abspath(files[0]);
	cap = Captcha(trainer, fname);
	cap.analyze();
	cap.view(origLabel, gradFixedLabel, croppedLabel, charLabel, divLabelFrame, divLabels, ansLabel);

def nextImage(event):
	onNext(False);

def _pack():
	origLabel.pack();
	gradFixedLabel.pack();
	croppedLabel.pack();
	charLabel.pack();
	for divLabel in divLabels:
		divLabel.pack(side='left');
	divLabelFrame.pack();
	ansLabel.pack();
	ansTxtLabel.pack();
	textLabel.pack();
if __name__ == '__main__':
	files = glob.glob("../image/*.jpg");
	random.shuffle(files);
	window = Tk();
	origLabel = Label(window)
	gradFixedLabel = Label(window)
	croppedLabel = Label(window);
	charLabel =Label(window)
	divLabelFrame = Frame(window);
	divLabels = [Label(divLabelFrame) for i in range(0,5)];
	ansLabel = Label(window, font=Font(size=36,weight="bold"), fg="#ff0000")
	ansTxtLabel = Label(window, text=u"答えはこれであってる？")
	textLabel = Entry(window, font=Font(size=36,weight="bold"), width=9);
	_pack();
	onNext(True);
	textLabel.bind("<Return>", nextImage);
	window.mainloop();

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob;
import os;

from Tkinter import Tk, Label, Frame, Entry;
from PIL import Image, ImageTk;

from analyzer.gravity import Gravity;
from analyzer.box import BoxDetect;
from analyzer.char import CharDetect;
from analyzer.neural import NeuralNet;
from analyzer.bayese import Bayese;

class Trainer(object):
	def __init__(self):
		self.neural = NeuralNet.load();
	def imageToList(self, image):
		w,h = image.size;
		dat = [0] * (w*h);
		cnt = 0
		for y in xrange(0, h):
			for x in xrange(0, w):
				r,g,b,_ = image.getpixel((x,y));
				if (r+g+b) < 230*3:
					dat[cnt]=1;
				else:
					dat[cnt] = 0;
				cnt+=1;
		return dat;
	def judge(self, image):
		dat = self.imageToList(image);
		return self.neural.judge(dat)

class Captcha(object):
	def __init__(self, trainer, fname):
		self.trainer = trainer;
		self.fname = fname;
		self.image = Image.open(fname);
	def analyze(self):
		#勾配を修正
		self.gravity = Gravity(self.image);
		self.gravity.analyze();
		#文字領域の切り出し
		self.box = BoxDetect(self.gravity.getImage(), self.gravity.getSupportLine());
		self.box.analyze();
		#文字の切り出し
		self.char = CharDetect(self.box.getImage(), NeuralNet.IN_SIZE_SQUARE);
		self.char.analyze();

		ans = [];
		for i in xrange(0, CharDetect.CHARACTERS):
			out = self.trainer.judge(self.char.getImage(i));
			
			ans.append(out);

	def setImage(self, label, image):
		tkImage = ImageTk.PhotoImage(image);
		label.configure(image = tkImage);
		label.image = tkImage;
		return label;
	def judge(self):
		pass
	def train(self, answer):
		pass
	def view(self, origLabel, gradFixedLabel, croppedLabel, charLabel, divLabelFrame, divLabels):
		self.setImage(origLabel, self.image).pack();
		self.setImage(gradFixedLabel, self.gravity.getDebugImage()).pack();
		self.setImage(croppedLabel, self.box.getDebugImage()).pack();
		self.setImage(charLabel, self.char.getDebugImage()).pack();
		for i in range(0, len(divLabels)):
			label = divLabels[i];
			self.setImage(label, self.char.getImage(i)).pack(side='left');
		divLabelFrame.pack();

def onNext(isFirst):
	ans = textLabel.get();
	textLabel.delete(0, len(ans));
	fname = os.path.abspath(files[0]);
	if(not isFirst):
		if len(ans) != 5:
			return;
		del files[0];
		fname = os.path.abspath(files[0]);
	cap = Captcha(trainer, fname);
	cap.analyze();
	cap.view(origLabel, gradFixedLabel, croppedLabel, charLabel, divLabelFrame, divLabels);

def nextImage(event):
	onNext(False);

if __name__ == '__main__':
	trainer = Trainer();
	files = glob.glob("../image/*.jpg");
	window = Tk();
	origLabel = Label(window);
	gradFixedLabel = Label(window);
	croppedLabel = Label(window);
	charLabel =Label(window);
	divLabelFrame = Frame(window);
	divLabels = [Label(divLabelFrame) for i in range(0,5)];
	textLabel = Entry(window);
	onNext(True);
	textLabel.pack();
	textLabel.bind("<Return>", nextImage);
	window.mainloop();

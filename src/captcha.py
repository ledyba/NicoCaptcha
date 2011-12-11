#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011/12/11

@author: psi
'''

from PIL import Image, ImageTk;

from analyzer.gravity import Gravity;
from analyzer.box import BoxDetect;
from analyzer.char import CharDetect;
from analyzer.neural import NeuralNet, IN_SIZE_SQUARE;
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
				if r+g+b < (230*3):
					dat[cnt]=1;
				else:
					dat[cnt] = 0;
				cnt+=1;
		return dat;
	def judge(self, image):
		dat = self.imageToList(image);
		ans = self.neural.judge(dat);
		_max = -1;
		maxIdx = -1;
		for i in range(0, len(ans)):
			if ans[i] > _max:
				_max = ans[i];
				maxIdx = i;
		return chr(maxIdx+97);
	def train(self, i, trueAlphabet):
		trueSignal = [0.0] * 26;
		trueSignal[ord(trueAlphabet)-97] = 1.0;
		self.neural.train(trueSignal);
	def save(self):
		self.neural.save();

class Captcha(object):
	def __init__(self, trainer, fname):
		self.trainer = trainer;
		self.fname = fname;
		self.image = Image.open(fname);
	def analyze(self, ans=None):
		#勾配を修正
		self.gravity = Gravity(self.image);
		self.gravity.analyze();
		#文字領域の切り出し
		self.box = BoxDetect(self.gravity.getImage(), self.gravity.getSupportLine());
		self.box.analyze();
		#文字の切り出し
		self.char = CharDetect(self.box.getImage(), IN_SIZE_SQUARE);
		self.char.analyze();

		answer = [];
		for i in xrange(0, CharDetect.CHARACTERS):
			out = self.trainer.judge(self.char.getImage(i));
			if ans != None:
				if ans[i] != out:
					self.trainer.train(i, ans[i]);
			answer.append(out);
		self.answer = "".join(answer);
		return self.answer
	def train(self, trueAnswer):
		for i in range(0, len(trueAnswer)):
			ans = self.trainer.judge(self.char.getImage(i));
			if ans != trueAnswer[i]:
				self.trainer.train(i, trueAnswer[i]);
	def setImage(self, label, image):
		tkImage = ImageTk.PhotoImage(image);
		label.configure(image = tkImage);
		label.image = tkImage;
		return label;
	def view(self, origLabel, gradFixedLabel, croppedLabel, charLabel, divLabelFrame, divLabels, ansLabel):
		self.setImage(origLabel, self.image)
		self.setImage(gradFixedLabel, self.gravity.getDebugImage())
		self.setImage(croppedLabel, self.box.getDebugImage())
		self.setImage(charLabel, self.char.getDebugImage())
		for i in range(0, len(divLabels)):
			label = divLabels[i];
			self.setImage(label, self.char.getImage(i))
		ansLabel["text"]  = self.answer;

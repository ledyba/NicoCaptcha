#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle;

class Neural(object):
	SIZE=32
	def __init__(self, _in=1024, _middle=1024, _out=26):
		pass
	def judge(self, image):
		pass
	def train(self, image, trueSignal):
		pass
	@staticmethod
	def load(cls, fname="neural.dat"):
		with open(fname,"r") as f:
			return pickle.load(f);
	def save(self, fname="neural.dat"):
		with open(fname,"w") as f:
			pickle.dump(self, f, -1)

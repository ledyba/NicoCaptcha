#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle;
import os;
class Bayese(object):
	def __init__(self, matrixSize=26):
		self.matrixSize = matrixSize;
		self.matrix = [0] * (matrixSize * matrixSize);
	def train(self, one, another, delta):
		self.matrix[one*self.matrixSize + another] += delta;
	def calc(self, one, another):
		total = 0;
		for i in xrange(one*self.matrixSize, (one+1)*self.matrixSize-1):
			total += self.matrix[i];
		return float(self.matrix[one*self.matrixSize + another])/total;
	@classmethod
	def load(cls, fname="bayese.dat"):
		if os.path.exists(fname):
			with open(fname,"rb") as f:
				return pickle.load(f);
		else:
			return Bayese();
	def save(self, fname="bayese.dat"):
		with open(self.fname, "wb") as f:
			f.write(pickle.dump(self, f, -1));

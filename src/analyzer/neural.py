#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle;
import math;
import os;

class Neuron(object):
	TRAIN_RATIO = 0.3;
	def __init__(self, inSize):
		self.inSize = inSize;
		self.weight = [1]*(inSize+1);
	def calcSum(self, data):
		_sum = self.weight[0]*1.0;
		assert len(data) == self.inSize;
		for i in xrange(0, self.inSize):
			_sum += self.weight[i+1] * data[i];
		return _sum;
	def fire(self, data):
		return self.sigmoid(self.calcSum(data));
	def train(self, data, trueSignal):
		output = self.fire(data);
		data = [0].extend(data);
		for i in xrange(0, self.inSize):
			self.weight[i] = self.weight[i] + Neuron.TRAIN_RATIO*(data[i]*(output-trueSignal) * output * (1-output));
	def sigmoid(self, x):
		return 1.0 / (1+math.exp(x));

class NeuralNet(object):
	IN_SIZE_SQUARE = 16;
	IN_SIZE=IN_SIZE_SQUARE**2;
	OUT_SIZE = 26
	def __init__(self, _in=IN_SIZE, _middle=IN_SIZE, _out=OUT_SIZE):
		self.middleSize = _middle;
		self.outSize = _out;
		self.middleNeurons = [None] * _middle;
		self.outNeurons = [None] * _out;
		for i in xrange(0, _middle):
			self.middleNeurons[i] = Neuron(_in);
		for i in xrange(0, _out):
			self.outNeurons[i] = Neuron(_middle);
	def judge(self, data):
		middleData = [None] * self.middleSize
		for i in xrange(0, self.middleSize):
			middleData[i] = self.middleNeurons[i].fire(data);
		outSignal = [None] * self.outSize;
		for i in xrange(0, self.outSize):
			outSignal[i] = self.outNeurons[i].fire(data);
		return outSignal;
	def train(self, data, trueSignal):
		pass
	@classmethod
	def load(cls, fname="bayese.dat"):
		if os.path.exists(fname):
			with open(fname,"r") as f:
				return pickle.load(f);
		else:
			return NeuralNet();
	def save(self, fname="neural.dat"):
		with open(fname,"w") as f:
			pickle.dump(self, f, -1)

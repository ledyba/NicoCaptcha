#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle;
import math;
import os;
import random;

TRAIN_RATIO = 0.3;
RANGE=1.0

class Neuron(object):
	def __init__(self, inSize, weight = None):
		self.inSize = inSize;
		if weight:
			self.weight = weight[:]
		else:
			self.weight = [None]*(inSize+1);
			for i in xrange(0, inSize+1):
				self.weight[i]=(random.random()*2.0*RANGE)-RANGE;
	def __repr__(self):
		return str(self.weight);
	def calcSum(self, data):
		_sum = self.weight[0]*1.0;
		assert len(data) == self.inSize;
		for i in xrange(0, self.inSize):
			_sum += self.weight[i+1] * data[i];
		return _sum;
	def fire(self, data):
		return self.sigmoid(self.calcSum(data));
	def train(self, data, output, outDelta, weightDeltas):
		p = outDelta * output * (1-output);
		self.weight[0] += TRAIN_RATIO*(1.0 * p)
		for i in xrange(0, self.inSize):
			weightDelta = data[i]*p;
			weightDeltas[i] += weightDelta * self.weight[i+1];
			self.weight[i+1] += TRAIN_RATIO*weightDelta;
		return weightDeltas;
	def sigmoid(self, x):
		return 1.0 / (1+math.exp(-x));

IN_SIZE_SQUARE = 16;
IN_SIZE=IN_SIZE_SQUARE**2;
OUT_SIZE = 26

class NeuralNet(object):
	def __init__(self, _in=IN_SIZE, _middle=IN_SIZE, _out=OUT_SIZE):
		self.inSize = _in;
		self.middleSize = _middle;
		self.outSize = _out;
		self.inputSignal = None;
		self.middleNeurons = [None] * _middle;
		self.outNeurons = [None] * _out;
		self.middleSignal = [None] * _middle;
		self.outSignal = [None] * _out;
		for i in xrange(0, _middle):
			self.middleNeurons[i] = Neuron(_in);
		for i in xrange(0, _out):
			self.outNeurons[i] = Neuron(_middle);
	def judge(self, data):
		self.inputSignal = data;
		for i in xrange(0, self.middleSize):
			self.middleSignal[i] = self.middleNeurons[i].fire(self.inputSignal);
		for i in xrange(0, self.outSize):
			self.outSignal[i] = self.outNeurons[i].fire(self.middleSignal);
		return self.outSignal[:];
	def train(self, trueSignal):
		middleDeltas = [0.0] * self.middleSize;
		for i in xrange(0, self.outSize):
			self.outNeurons[i].train(self.middleSignal, self.outSignal[i], trueSignal[i]-self.outSignal[i], middleDeltas);
		inDeltas = [0.0] * self.inSize;
		for i in xrange(0, self.middleSize):
			self.middleNeurons[i].train(self.inputSignal, self.middleSignal[i], middleDeltas[i], inDeltas);
	@classmethod
	def load(cls, fname="neural.dat"):
		if os.path.exists(fname):
			with open(fname,"rb") as f:
				return pickle.load(f);
		else:
			return NeuralNet();
	def save(self, fname="neural.dat"):
		with open(fname,"wb") as f:
			pickle.dump(self, f, -1)
			
total = 0
succeeded = 0
def _test(neural, train):
	global total, succeeded;
	for item in train:
		_max = -1;
		_maxIdx = -1;
		ans = neural.judge(item[0])
		for j in xrange(0, len(ans)):
			if _max <= ans[j]:
				_max = ans[j];
				_maxIdx = j;
		total += 1
		if item[1][_maxIdx] != 1:
			print "missed!", item[1], "!=", _maxIdx
			neural.train(item[1]);
		else:
			succeeded += 1
			print "succeeded", _maxIdx
def _main(*argv):
	if os.path.exists("test.dat"):
		neural = NeuralNet.load("test.dat");
	else:
		neural = NeuralNet(4, 4, 4);
	train = [
		[[0,0,0,1],[0,0,0,1]],
		[[0,0,1,0],[0,0,1,0]],
		[[0,1,0,0],[0,1,0,0]],
		[[1,0,0,0],[1,0,0,0]],
	];
	for _ in xrange(0, 100000):
		random.shuffle(train);
		_test(neural, [train[1]]);
	_test(neural, [train[1]]);
	neural.save("test.dat");
	print "ended",float(succeeded*100)/total,"%"
if __name__ == '__main__':
	import sys;
	_main(sys.argv);

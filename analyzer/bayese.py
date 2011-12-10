#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      psi
#
# Created:     10/12/2011
# Copyright:   (c) psi 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pickle;
import sys;
import os;
class Bayes(object):
    def __init__(self, fname="bayese.dat", matrixSize=26):
        self.fname=fname;
        if os.path.exists(self.fname):
            with open(self.fname) as f:
                self.matrix = pickle.load(f);
        else:
            self.matrix = {
                size:matrixSize,
                matrix: [0] * (self.matrixSize * self.matrixSize)
            }
    def train(self, one, another, delta):
        self.matrix[one*self.matrixSize + another] += delta;
    def calc(self, one, another):
        total = sum(self.matrix[one*self.matrixSize:(one+1)*self.matrixSize-1]);
        return float(self.matrix[one*self.matrixSize + another])/total;
    def save(self):
        with open(self.fname, "w") as f:
            f.write(pickle.dump(self.matrix, f, 2));

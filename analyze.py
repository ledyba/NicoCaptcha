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
import random;
import math;

from Tkinter import Tk, Label, Frame, Entry;
from PIL import Image, ImageTk, ImageFilter, ImageDraw;

from analyzer.gravity import Gravity;
from analyzer.box import BoxDetect;
from analyzer.char import CharDetect;
from analyzer.neural import Neural;

class Captcha(object):
    def __init__(self, fname):
        self.fname = fname;
        self.image = Image.open(fname);
    def analyze(self):
        #勾配を修正
        self.gravity = Gravity(self.image);
        self.gravity.analyze();
        #文字領域の切り出し
        self.box = BoxDetect(self.gravity.getImage(), self.gravity.getSupportLine());
        self.box.analyze();
        #TODO: 文字の切り出し
        self.char = CharDetect(self.box.getImage(), Neural.SIZE);
        self.char.analyze();
        #ニューラルネットワーク！

    def setImage(self, label, image):
        tkImage = ImageTk.PhotoImage(image);
        label.configure(image = tkImage);
        label.image = tkImage;
        return label;

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
    cap = Captcha(fname);
    cap.analyze();
    cap.view(origLabel, gradFixedLabel, croppedLabel, charLabel, divLabelFrame, divLabels);

def next(event):
    onNext(False);

if __name__ == '__main__':
    files = glob.glob("./image/*.jpg");
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
    textLabel.bind("<Return>", next);
    window.mainloop();

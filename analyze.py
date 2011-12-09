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
from Tkinter import Tk, Label;
from PIL import Image, ImageTk, ImageFilter, ImageDraw;

class Neural(object):
    pass

class Captcha(object):
    def __init__(self, fname, debug = False):
        self.fname = fname;
        self.image = Image.open(fname);
        self.debug = debug;
    def analyze(self):
        #勾配を修正
        self.gradFixedImage, vector = self.fixGrad(self.image);
        print vector
        #TODO: 文字の切り出し
        self.croppedImage = self.detectBox(self.gradFixedImage, vector);
        #ニューラルネットワーク！

    """
        勾配を修正する
    """
    def fixGrad(self, image):
        processed = image \
            .filter(ImageFilter.MaxFilter) \
            .filter(ImageFilter.MinFilter) \
            ;
        pts = self.gravity(processed);
        pts.sort();
        rot = 0.0;
        for pt in pts[1:]:
            deltaY = pt[1]-pts[0][1];
            deltaX = pt[0]-pts[0][0];
            rot += math.atan2(deltaY, deltaX);
        rot /= len(pts)-1;
        processed = processed.rotate(math.degrees(rot), Image.BICUBIC)
        #ポイントもそれにつれて回転
        w,h = processed.size;
        w/=2.0;
        h/=2.0;
        sin_ = math.sin(-rot);
        cos_ = math.cos(-rot);
        for pt in pts:
            pt[0] = cos_*(pt[0]-w) - sin_*(pt[1]-h) + w;
            pt[1] = sin_*(pt[0]-w) + cos_*(pt[1]-h) + h;
        #中央線を表示
        if self.debug:
            draw = ImageDraw.Draw(processed);
            ptInt = [(int(pt[0]), int(pt[1])) for pt in pts]
            draw.line(ptInt, fill="#ff0000", width=3);
            del draw;
        return processed, [tuple(pt[0:2]) for pt in pts];
    POWER = math.exp(8);
    def calcForce(self, pt, other, isSigmoid=False):
        deltaX = other[0]-pt[0];
        deltaY = other[1]-pt[1];
        distance = (deltaX**2+deltaY**2)+100;
        distanceSqrt = math.sqrt(distance);
        if isSigmoid:
            force = -1.0/(0.1+math.pow(Captcha.POWER,distanceSqrt-other[2]))
        else:
            force = other[2]/distanceSqrt;
        return (force * deltaX / distanceSqrt, force * deltaY / distanceSqrt)
    def update_pts(self, pt, stones, others):
        fx = fy = 0.0;
        gx = gy = 0.0;
        for other in others:
            if other == pt:
                continue
            x, y = self.calcForce(pt, other, True);
            gx += x;
            gy += y;

        for stone in stones:
            x, y = self.calcForce(pt, stone, False);
            fx += x;
            fy += y;

        pt[0] += fx + gx;
        pt[1] += fy + gy;
        return fx ** 2 + fy ** 2;
    def gravity_stage(self, pts, stones):
        fsum = 0;
        for pt in pts:
            fsum += self.update_pts(pt, stones, pts);
        return fsum / len(pts);
    def getStones(self, image):
        stones = [];
        w,h = image.size;
        for y in range(0, h):
            for x in range(0, w):
                r,g,b = image.getpixel((x,y))
                weight = (255*3-(r+g+b)) / (3.0 * 255);
                if weight > 0.1:
                    stones.append((x,y,1.0));
        return stones;
    def gravity(self, image):
        w,h = image.size;
        pt_weight = w/2.0;
        stones = self.getStones(image);
        min_ = min(w*w,h*h) / (10.0**5);

        pts = [
                [0, h/2, pt_weight],
                [w, h/2, pt_weight],
        ];
        lastForce = 0.0;
        for i in xrange(0, 100):
            force = self.gravity_stage(pts, stones);
            delta = abs(force-lastForce);
            lastForce = force;
            if delta < min_ and i > 30:
                print delta, "<>", min_;
                break;
        return pts;
    def detectBox(self, image, vector):
        w,h = image.size;
    def updateBox(self, image, a, b):
        pass
    def view(self, label):
        tkImg = ImageTk.PhotoImage(self.gradFixedImage);
        label.configure(image = tkImg);
        label.image = tkImg;
        label.pack();

def onNext(isFirst):
    fname = os.path.abspath(files[0]);
    if(not isFirst):
        del files[0];
        fname = os.path.abspath(files[0]);
    cap = Captcha(fname, True);
    cap.analyze();
    cap.view(label);

def next(event):
    onNext(False);

if __name__ == '__main__':
    files = glob.glob("./image/*.jpg");
    window = Tk();
    window.bind_all("<Return>", next);
    label = Label(window);
    onNext(True);
    window.mainloop();

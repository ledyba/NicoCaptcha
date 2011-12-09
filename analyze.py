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
        self.whiteImage= Image.new("RGBA", self.image.size, (255,255,255,255))
        self.debug = debug;
    def analyze(self):
        #勾配を修正
        self.gradFixedImage, vector = self.fixGrad(self.image);
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
            .convert("RGBA") \
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
        processed = Image.composite(processed, self.whiteImage, processed)
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
        return processed, [tuple(int(v) for v in pt[0:2]) for pt in pts];
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
                r,g,b,a = image.getpixel((x,y))
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
        minSize = w / 4;
        va, vb = vector;
        width = vb[0]-va[0]
        vec = None;
        if width < minSize:
            fix = (minSize - width) / 2;
            vec = [va[0]-fix, va[1], vb[0]+fix, va[1]];
        else:
            vec = [va[0], va[1], vb[0], vb[1]];
        extended = 1;
        while extended > 0:
            extended = 0;
            extended += self.updateBox(image, vec, ( 0,  0,  0,  1));
            extended += self.updateBox(image, vec, (-1,  0,  0,  0));
            extended += self.updateBox(image, vec, ( 0, -1,  0,  0));
            extended += self.updateBox(image, vec, ( 0,  0,  1,  0));
        if self.debug:
            draw = ImageDraw.Draw(image);
            draw.rectangle(vec, outline="#ff0000");
            del draw;
    MARGIN = 10;
    def updateBox(self, image, vec, fixVec):
        outBound = False;
        contCnt = 0;
        extended = 0;
        w,h = image.size;
        total=0;
        while contCnt < Captcha.MARGIN:
            if vec[0]+fixVec[0] < 0 or vec[1]+fixVec[1] < 0 or vec[2]+fixVec[2] >= w or vec[3]+fixVec[3] >=h:
                outBound = True;
                break;
            total += 1;
            if self.updateBoxStage(image, vec, fixVec) <= 0:
                contCnt+=1;
            else:
                contCnt = 0;
            extended+=1;
        if outBound:
            over = contCnt;
        else:
            over = Captcha.MARGIN;
        for i in range(0, len(vec)):
            vec[i] -= (fixVec[i] * over);
        extended -= over;
        return extended;
    def updateBoxStage(self, image, vec, fixVec):
        for i in xrange(0, len(vec)):
            delta = fixVec[i];
            vec[i] += delta;
            pos = vec[i];
            changed1 = (i+1) % 2;
            changed2 = changed1+2 % 4;
            _from = min(vec[changed1], vec[changed2]);
            _to = max(vec[changed1], vec[changed2]);
            isX = (i % 2) == 0;
            blackCount = 0;
            if delta != 0:
                for j in xrange(_from, _to+1):
                    if isX:
                        pix = image.getpixel((pos, j));
                    else:
                        pix = image.getpixel((j, pos));
                    r,g,b,a = pix;
                    pix = 1-((r+g+b) / 3.0 / 255.0);
                    if pix > 0.1:
                        blackCount+=1;
                return blackCount;
        return None;
    def view(self, origLabel, gradFixedLabel):
        tkImage = ImageTk.PhotoImage(self.image);
        origLabel.configure(image = tkImage);
        origLabel.image = tkImage;
        origLabel.pack();
        tkGradFixedImage = ImageTk.PhotoImage(self.gradFixedImage);
        gradFixedLabel.configure(image = tkGradFixedImage);
        gradFixedLabel.image = tkGradFixedImage;
        gradFixedLabel.pack();

def onNext(isFirst):
    fname = os.path.abspath(files[0]);
    if(not isFirst):
        del files[0];
        fname = os.path.abspath(files[0]);
    cap = Captcha(fname, True);
    cap.analyze();
    cap.view(origLabel, gradFixedLabel);

def next(event):
    onNext(False);

if __name__ == '__main__':
    files = glob.glob("./image/*.jpg");
    window = Tk();
    window.bind_all("<Return>", next);
    origLabel = Label(window);
    gradFixedLabel = Label(window);
    onNext(True);
    window.mainloop();

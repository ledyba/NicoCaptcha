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
        self.processed = self.image.filter(ImageFilter.DETAIL).filter(ImageFilter.ModeFilter())
        self.debug= debug;
    def analyze(self):
        #勾配を修正
        self.fixGrad();
        #TODO: 文字の切り出し
        #ニューラルネットワーク！

    """
        勾配を修正する
    """
    def fixGrad(self):
        pts = self.gravity(self.processed);
        pts.sort();
        if self.debug:
            draw = ImageDraw.Draw(self.processed);
            ptInt = [(int(pt[0]), int(pt[1])) for pt in pts]
            draw.line(ptInt, fill="#ff0000", width=3);
            del draw;
        deltaY = pts[1][1]-pts[0][1];
        deltaX = pts[1][0]-pts[0][0];
        rot = math.atan2(deltaY, deltaX) * 180 / math.pi;
        self.processed = self.processed.rotate(rot, Image.BICUBIC)

    def calcForce(self, pt, other):
        deltaX = other[0]-pt[0];
        deltaY = other[1]-pt[1];
        distance = deltaX**2+deltaY**2;
        distanceSqrt = math.sqrt(distance);
        force = other[2]/distanceSqrt;
        #force = 2.0*other[2]/(1+math.pow(1.01, distanceSqrt))
        #if force > 600.0:
        #    print force
        return (force * deltaX / distanceSqrt, force * deltaY / distanceSqrt)

    def update_pts(self, pt, stones, others):
        fx = fy = 0.0;
        for other in others:
            if other == pt:
                continue
            x, y = self.calcForce(pt, other);
            fx += x;
            fy += y;

        for stone in stones:
            x, y = self.calcForce(pt, stone);
            fx += x;
            fy += y;

        pt[0] += fx;
        pt[1] += fy;
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
                    stones.append((x,y,weight/5.0));
        return stones;
    def gravity(self, image):
        w,h = image.size;
        pt_weight = 1/(2.0/3.0)**2;
        stones = self.getStones(image);
        min_ = min(w*w,h*h) / (100.0**3);

        pts = [[0, h/2, pt_weight], [w, h/2, pt_weight]];
        for i in xrange(0, 50):
            delta = self.gravity_stage(pts, stones);
            print delta;
            if delta < min_:
                break;
        return pts;
    def view(self):
        window = Tk();
        tkImg = ImageTk.PhotoImage(self.processed);
        label = Label(window, image = tkImg)
        label.pack();
        window.mainloop();


def main():
    cap = Captcha("./renamed/ceast.png", True);
    cap.analyze();
    cap.view();

if __name__ == '__main__':
    main()

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

MARGIN=20
def updateBoxStage(image, vec, fixVec):
    for i in xrange(0, len(vec)):
        if fixVec[i] != 0:
            vec[i] += fixVec[i];
            pos = vec[i];
            changed1 = (i+1) % 2;
            changed2 = changed1+2 % 4;
            _from = min(vec[changed1], vec[changed2]);
            _to = max(vec[changed1], vec[changed2]);
            isX = (i % 2) == 0;
            blackCount = 0;
            for j in xrange(_from, _to+1):
                if isX:
                    pix = image.getpixel((pos, j));
                else:
                    try:
                        pix = image.getpixel((j, pos));
                    except:
                        print vec;
                        print (j, pos),"<>",image.size;
                r,g,b,a = pix;
                pix = 1-((r+g+b) / 3.0 / 255.0);
                if pix > 0.1:
                    blackCount+=1;
            return blackCount;
    raise ValueError("Please do not input empty vector");

def updateBox(image, vec, fixVec):
    outBound = False;
    contCnt = 0;
    extended = 0;
    w,h = image.size;
    total=0;
    while contCnt < MARGIN:
        if vec[0]+fixVec[0] < 0 or vec[1]+fixVec[1] < 0 or vec[2]+fixVec[2] >= w or vec[3]+fixVec[3] >=h:
            outBound = True;
            break;
        total += 1;
        if updateBoxStage(image, vec, fixVec) <= 0:
            contCnt+=1;
        else:
            contCnt = 0;
        extended+=1;
    for i in range(0, len(vec)):
        vec[i] -= (fixVec[i] * (contCnt));
    extended -= contCnt;
    return extended;